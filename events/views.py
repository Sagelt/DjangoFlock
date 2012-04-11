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
from events.forms import GameForm, EventForm
from events.models import Event, Game, Publisher
from events.resources import EventResource
from datetime import datetime, MAXYEAR

class PublisherRoot(ListOrCreateModelView):
    permissions = (IsUserOrIsAnonReadOnly, )

class PublisherModelView(InstanceModelView):
    permissions = (IsUserOrIsAnonReadOnly, )

class GameRoot(ListOrCreateModelView):
    permissions = (IsUserOrIsAnonReadOnly, )

class GameModelView(InstanceModelView):
    permissions = (IsUserOrIsAnonReadOnly, )

class EventRoot(ListOrCreateModelView):
    form = EventForm
    permissions = (IsUserOrIsAnonReadOnly, )
    
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
        Create new event
        """
        if self.user.is_authenticated():
            host = self.user
        else:
            raise PermissionDenied
        start = self.CONTENT['start']
        end = self.CONTENT['end']
        min = self.CONTENT['min']
        max = self.CONTENT['max']
        game = self.CONTENT['game']
        event = Event(host=host,
                      start=start,
                      end=end,
                      min=min,
                      max=max,
                      game=game)
        event.save()
        event_id = event.id
        return Response(status.HTTP_201_CREATED,
                        headers={'Location': reverse('event-instance', args=[event_id])})

class EventModelView(InstanceModelView):
    form = EventForm
    permissions = (IsUserOrIsAnonReadOnly, )
    
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
