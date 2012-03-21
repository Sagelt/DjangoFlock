from django.contrib.auth.models import User
from djangorestframework.resources import ModelResource
from events.models import Game, Event

class UserResource(ModelResource):
    model = User
    fields = ('username', 'first_name', 'last_name')

class GameResource(ModelResource):
    model = Game
    
class EventResource(ModelResource):
    model = Event
    ordering = ('start', )
    fields = (('host', UserResource),
              ('players', UserResource), ('game', GameResource),
              'start', 'end', 'min', 'max', 'join', 'leave', 'url')
    
    def join(self, instance):
        # TODO How hackish is this?
        return self.url(instance) + "join/"
    
    def leave(self, instance):
        # TODO How hackish is this?
        return self.url(instance) + "leave/"