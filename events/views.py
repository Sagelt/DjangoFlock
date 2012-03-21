from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from djangorestframework import status
from djangorestframework.permissions import IsUserOrIsAnonReadOnly, \
    IsAuthenticated
from djangorestframework.response import Response
from djangorestframework.views import View, InstanceModelView, \
    ListOrCreateModelView
from events.exceptions import EventFullException, OwnEventException
from events.forms import EventForm
from events.models import Event

class GameRoot(ListOrCreateModelView):
    permissions = (IsUserOrIsAnonReadOnly, )

class GameModelView(InstanceModelView):
    permissions = (IsUserOrIsAnonReadOnly, )

class EventRoot(View):
    """
    """
    form = EventForm
    permissions = (IsUserOrIsAnonReadOnly, )
    
    def get(self, request):
        """
        List all events.
        """
        events = Event.objects.all().order_by('start')
        return [reverse('event-instance', args=[event.id]) for event in events]
        
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