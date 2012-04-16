from datetime import datetime, MAXYEAR
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
        result = super(EventRoot, self).get(request)
        if 'start' in request.GET or 'end' in request.GET:
            try:
                start = datetime.fromtimestamp(int(request.GET['start']))
            except (KeyError, ValueError):
                start = datetime.fromtimestamp(0)
            try:
                end = datetime.fromtimestamp(int(request.GET['end']))
            except (KeyError, ValueError):
                end = datetime(MAXYEAR, 1, 1)
            result = result.filter(start__gt=start, end__lt=end)
        if 'player' in request.GET:
            try:
                user = User.objects.get(username=request.GET['player'])
            except User.DoesNotExist:
                user = None
            if user is not None:
                result = result.filter(players=user)
        if 'host' in request.GET:
            try:
                user = User.objects.get(username=request.GET['host'])
            except User.DoesNotExist:
                user = None
            if user is not None:
                result = result.filter(host=user)
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
