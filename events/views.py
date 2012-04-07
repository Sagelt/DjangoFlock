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

class HTMLRenderer(TemplateRenderer):
    media_type = 'text/html'
    
class PublisherListHTMLRenderer(HTMLRenderer):
    template = 'events/publisher_list.html'

class PublisherInstanceHTMLRenderer(HTMLRenderer):
    template = 'events/publisher.html'

class PublisherRoot(ListOrCreateModelView):
    permissions = (IsUserOrIsAnonReadOnly, )
    renderers = (DocumentingPlainTextRenderer, JSONRenderer,
                 JSONPRenderer, PublisherListHTMLRenderer, XMLRenderer)

class PublisherModelView(InstanceModelView):
    permissions = (IsUserOrIsAnonReadOnly, )
    renderers = (DocumentingPlainTextRenderer, JSONRenderer,
                 JSONPRenderer, PublisherInstanceHTMLRenderer, XMLRenderer)

class GameListHTMLRenderer(HTMLRenderer):
    template = 'events/game_list.html'

class GameInstanceHTMLRenderer(HTMLRenderer):
    template = 'events/game.html'

class GameCreate(CreateView):
    form_class = GameForm
    template_name = 'events/game_create.html'
    success_url = "/games/%(id)s/"
    model = Game
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameCreate, self).dispatch(*args, **kwargs)
    
class GameUpdate(UpdateView):
    form_class = GameForm
    template_name = 'events/game_update.html'
    success_url = '/games/%(id)s/'
    model = Game
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameUpdate, self).dispatch(*args, **kwargs)
    
class GameDelete(DeleteView):
    template_name = 'events/game_delete.html'
    model = Game
    success_url = '/games/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameDelete, self).dispatch(*args, **kwargs)

class GameRoot(ListOrCreateModelView):
    permissions = (IsUserOrIsAnonReadOnly, )
    renderers = (DocumentingPlainTextRenderer, JSONRenderer,
                 JSONPRenderer, GameListHTMLRenderer, XMLRenderer)

class GameModelView(InstanceModelView):
    permissions = (IsUserOrIsAnonReadOnly, )
    renderers = (DocumentingPlainTextRenderer, JSONRenderer,
                 JSONPRenderer, GameInstanceHTMLRenderer, XMLRenderer)

class EventListHTMLRenderer(HTMLRenderer):
    template = 'events/event_list.html'

class EventInstanceHTMLRenderer(HTMLRenderer):
    template = 'events/event.html'

    def render(self, obj=None, media_type=None):
        """
        Renders *obj* using the :attr:`template` specified on the class.
        
        Injects another variable into the context. 
        """
        if obj is None:
            return ''
        template = loader.get_template(self.template)
        players = [u['username'] for u in obj['players']]
        context = RequestContext(self.view.request, {'object': obj, 'players': players})
        return template.render(context)

class EventRoot(ListOrCreateModelView):
    form = EventForm
    permissions = (IsUserOrIsAnonReadOnly, )
    renderers = (DocumentingPlainTextRenderer, JSONRenderer,
                 JSONPRenderer, EventListHTMLRenderer, XMLRenderer)
    
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
    renderers = (DocumentingPlainTextRenderer, JSONRenderer,
                 JSONPRenderer, EventInstanceHTMLRenderer, XMLRenderer)
    
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
    
class EventCreate(CreateView):
    form_class = EventForm
    template_name = 'events/event_create.html'
    success_url = "/events/%(id)s/"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventCreate, self).dispatch(*args, **kwargs)
    
    def get_form_kwargs(self, **kwargs):
        """
        Extends `get_form_kwargs` to add an instance variable with the host set,
        since this is not a form-submittable part of an Event. See the note at
        https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#using-a
        -subset-of-fields-on-the-form for more information.
        """
        kwargs = super(EventCreate, self).get_form_kwargs(**kwargs)
        event = Event(host=self.request.user)
        kwargs['instance'] = event
        return kwargs

class EventUpdate(UpdateView):
    form_class = EventForm
    template_name = 'events/event_update.html'
    success_url = '/events/%(id)s/'
    model = Event
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        event = Event.objects.get(pk=kwargs['pk']) # Should exist. Will server error if not.
        request = args[0] # Should be the request, will server error on next line if not.
        if event.host == request.user:
            return super(EventUpdate, self).dispatch(*args, **kwargs)
        raise PermissionDenied
    
class EventDelete(DeleteView):
    template_name = 'events/event_delete.html'
    model = Event
    success_url = '/events/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        event = Event.objects.get(pk=kwargs['pk']) # Should exist. Will server error if not.
        request = args[0] # Should be the request, will server error on next line if not.
        if event.host == request.user:
            return super(EventDelete, self).dispatch(*args, **kwargs)
        raise PermissionDenied
