from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from djangorestframework import status
from djangorestframework.views import View, InstanceModelView
from djangorestframework.response import Response
from djangorestframework.permissions import IsUserOrIsAnonReadOnly
from events.models import Event
from events.forms import EventForm

class EventRoot(View):
    """
    """
    form = EventForm
    
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
        if request.user.is_authenticated():
            gm = request.user
        else:
            raise PermissionDenied
        start = self.CONTENT['start']
        end = self.CONTENT['end']
        min = self.CONTENT['min']
        max = self.CONTENT['max']
        game = self.CONTENT['game']
        event = Event(gm=gm,
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