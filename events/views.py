from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from djangorestframework import status
from djangorestframework.permissions import IsUserOrIsAnonReadOnly, \
    IsAuthenticated
from djangorestframework.renderers import TemplateRenderer, JSONRenderer, \
    JSONPRenderer, XMLRenderer, DocumentingPlainTextRenderer
from djangorestframework.response import Response
from djangorestframework.views import View, InstanceModelView, \
    ListOrCreateModelView
from events.exceptions import EventFullError, OwnEventError
from events.forms import EventForm, VoteForm
from events.models import Event, Game, Publisher, Convention
from events.resources import EventResource, VoteResource

class ApiRoot(View):
    def get(self, request):
        return [{'name': 'Publishers', 'url': reverse('publisher-list')},
                {'name': 'Games', 'url': reverse('game-list')},
                {'name': 'Conventions', 'url': reverse('convention-list')},
                {'name': 'Events', 'url': reverse('event-list')},
                {'name': 'Votes', 'url': reverse('vote-list')}]

class VoteRoot(ListOrCreateModelView):
    form = VoteForm
    permissions = (IsUserOrIsAnonReadOnly, )
    resource = VoteResource
    
    def get(self, request):
        """
        This shows votes-per-game in little hour boxes.
        
        It accepts many query parameters:
         - List of game IDs; if none, all games shown
         - Start timestamp: all votes that end after this will be included.
         - End timestamp: all votes that start before this will be included.
        """
        kwargs = {}
        if 'start' in request.GET:
            try:
                start = datetime.fromtimestamp(int(request.GET['start']))
            except (KeyError, ValueError):
                start = None
            if start is not None:
                kwargs['end__gte'] = start
        if 'end' in request.GET:
            try:
                end = datetime.fromtimestamp(int(request.GET['end']))
            except (KeyError, ValueError):
                end = None
            if end is not None:
                kwargs['start__lte'] = end
        if 'game' in request.GET:
            kwargs['game__in'] = []
            for value in request.GET.getlist('game'):
                try:
                    game = Game.objects.get(pk=value)
                    kwargs['game__in'].append(game)
                except Game.DoesNotExist:
                    pass
        # **kwargs gets passed to a filter on the queryset
        return super(VoteRoot, self).get(request, **kwargs)

    def post(self, request):
        """
        Create new vote.
        
        This just fiddles with self.CONTENT, to insert the currently
        authenticated user as the user.
        """
        if self.user.is_authenticated():
            self.CONTENT['user'] = self.user
        else:
            raise PermissionDenied
        return super(VoteRoot, self).post(request)

class VoteModelView(InstanceModelView):
    form = VoteForm
    permissions = (IsUserOrIsAnonReadOnly, )
    resource = VoteResource
    
    def delete(self, request, pk):
        event = get_object_or_404(Vote, pk=pk)
        if self.user == vote.user:
            return super(VoteModelView, self).delete(self, request, pk=pk)
        else:
            return Response(status.HTTP_403_FORBIDDEN, content='You do not have permission to delete this vote.')
        
    def put(self, request, pk):
        return Response(status.HTTP_501_NOT_IMPLEMENTED, content='Votes are immutable.')

class EventRoot(ListOrCreateModelView):
    form = EventForm
    permissions = (IsUserOrIsAnonReadOnly, )
    resource = EventResource
    
    def get(self, request):
        kwargs = {}
        if 'start' in request.GET:
            try:
                start = datetime.fromtimestamp(int(request.GET['start']))
            except (KeyError, ValueError):
                start = None
            if start is not None:
                kwargs['start__gte'] = start
        if 'end' in request.GET:
            try:
                end = datetime.fromtimestamp(int(request.GET['end']))
            except (KeyError, ValueError):
                end = None
            if end is not None:
                kwargs['end__lte'] = end
        if 'player' in request.GET:
            kwargs['players__in'] = []
            for value in request.GET.getlist('player'):
                try:
                    user = User.objects.get(username=value)
                    kwargs['players__in'].append(user)
                except User.DoesNotExist:
                    pass
        if 'host' in request.GET:
            kwargs['host__in'] = []
            for value in request.GET.getlist('host'):
                try:
                    user = User.objects.get(username=value)
                    kwargs['host__in'].append(user)
                except User.DoesNotExist:
                    pass
        result = super(EventRoot, self).get(request, **kwargs)
        return result
    
    def post(self, request):
        """
        Create new event.
        
        This just fiddles with self.CONTENT, to insert the currently
        authenticated user as the host.
        """
        if self.user.is_authenticated():
            self.CONTENT['host'] = self.user
        else:
            raise PermissionDenied
        return super(EventRoot, self).post(request)

class EventModelView(InstanceModelView):
    form = EventForm
    permissions = (IsUserOrIsAnonReadOnly, )
    resource = EventResource
    
    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if self.user == event.host:
            return super(EventModelView, self).delete(self, request, pk=pk)
        else:
            return Response(status.HTTP_403_FORBIDDEN, content='You do not have permission to delete this event.')
        
    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if self.user == event.host:
            return super(EventModelView, self).put(self, request, pk=pk)
        else:
            return Response(status.HTTP_403_FORBIDDEN, content='You do not have permission to edit this event.')
    
class EventJoinView(View):
    permissions = (IsAuthenticated, )
    resource = EventResource
    
    def get(self, request, pk):
        """
        Just passes through to .post so that the web interface works.
        """
        self.post(request, pk)
        return redirect('/events/%s/' % pk)
    
    def post(self, request, pk):
        user = self.user # Given the permissions setting, should always be authenticated.
        event = get_object_or_404(Event, pk=pk)
        try:
            event.add_player(user)
            return Response(status.HTTP_201_CREATED,
                            headers={'Location': reverse('event-instance', args=[event.id])})
        except OwnEventError:
            return Response(status.HTTP_403_FORBIDDEN, content='You own this event.')
        except EventFullError:
            return Response(status.HTTP_403_FORBIDDEN, content='This event is full.')
        except ValueError:
            return Response(status.HTTP_403_FORBIDDEN, content='You do not have permission to join this event.')
    
class EventLeaveView(View):
    permissions = (IsAuthenticated, )
    resource = EventResource

    def get(self, request, pk):
        """
        Just passes through to .post so that the web interface works.
        """
        self.post(request, pk)
        return redirect('/events/%s/' % pk)
    
    def post(self, request, pk):
        user = self.user # Given the permissions setting, should always be authenticated
        event = get_object_or_404(Event, pk=pk)
        event.remove_player(user)
        return Response(status.HTTP_204_NO_CONTENT)
