from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
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
from events.exceptions import EventFullException, OwnEventException
from events.forms import GameForm, EventForm
from events.models import Event, Game
from events.resources import EventResource

class HTMLRenderer(TemplateRenderer):
    media_type = 'text/html'

class GameListHTMLRenderer(HTMLRenderer):
    template = 'events/game_list.html'

class GameInstanceHTMLRenderer(HTMLRenderer):
    template = 'events/game.html'
    
class GameCreate(CreateView):
    form_class = GameForm
    template_name = 'events/game_create.html'
    success_url = "/games/%(id)s/"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameCreate, self).dispatch(*args, **kwargs)

class GameUpdate(UpdateView):
    form_class = GameForm
    template_name = 'events/game_update.html'
    success_url = '/games/%(id)s/'
    model = Game
    
    # This currently redirects to login, even for logged in users, if they lack
    # permission. That's ugly behavior.
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(GameUpdate, self).dispatch(*args, **kwargs)
    
class GameDelete(DeleteView):
    template_name = 'events/game_delete.html'
    model = Game
    success_url = '/games/'
    
    # This currently redirects to login, even for logged in users, if they lack
    # permission. That's ugly behavior.
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(GameDelete, self).dispatch(*args, **kwargs)

class EventListHTMLRenderer(HTMLRenderer):
    template = 'events/event_list.html'

class EventInstanceHTMLRenderer(HTMLRenderer):
    template = 'events/event.html'

class GameRoot(ListOrCreateModelView):
    permissions = (IsUserOrIsAnonReadOnly, )
    renderers = (GameListHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer,
                 DocumentingPlainTextRenderer)

class GameModelView(InstanceModelView):
    permissions = (IsUserOrIsAnonReadOnly, )
    renderers = (GameInstanceHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer,
                 DocumentingPlainTextRenderer)

class EventRoot(ListOrCreateModelView):
    form = EventForm
    permissions = (IsUserOrIsAnonReadOnly, )
    renderers = (EventListHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer,
                 DocumentingPlainTextRenderer)
    
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
    renderers = (EventInstanceHTMLRenderer, JSONRenderer, JSONPRenderer, XMLRenderer,
                 DocumentingPlainTextRenderer)
    
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
    
    def post(self, request, pk):
        user = self.user # Given the permissions setting, should always be authenticated.
        event = get_object_or_404(Event, pk=pk)
        try:
            event.add_player(user)
            return Response(status.HTTP_201_CREATED,
                            headers={'Location': reverse('event-instance', args=[event.id])})
        except OwnEventException:
            return Response(status.HTTP_403_FORBIDDEN, content='You own this event.')
        except EventFullException:
            return Response(status.HTTP_403_FORBIDDEN, content='This event is full.')
        except ValueError:
            return Response(status.HTTP_403_FORBIDDEN, content='You do not have permission to join this event.')
    
class EventLeaveView(View):
    permissions = (IsAuthenticated, )
    
    def post(self, request, pk):
        user = self.user # Given the permissions setting, should always be authenticated
        event = get_object_or_404(Event, pk=pk)
        event.remove_player(user)
        return Response(status.HTTP_204_NO_CONTENT)