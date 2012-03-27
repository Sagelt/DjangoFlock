from django.contrib.auth.models import User
from djangorestframework.resources import ModelResource
from events.models import Game, Event, Publisher

class UserResource(ModelResource):
    model = User
    ordering = ('username', )
    fields = ('username', 'first_name', 'last_name')

class PublisherResource(ModelResource):
    model = Publisher
    ordering = ('name', )
    fields = ('name', 'publisher_url', 'url')

class GameResource(ModelResource):
    model = Game
    ordering = ('name', )
    fields = ('name', 'edition', 'publisher')
    
class EventResource(ModelResource):
    model = Event
    ordering = ('start', )
    fields = (('host', UserResource),
              ('players', UserResource), ('game', GameResource),
              'start', 'end', 'min', 'max', 'join', 'leave', 'url', 'duration')
    
    def join(self, instance):
        # TODO How hackish is this?
        return self.url(instance) + "join/"
    
    def leave(self, instance):
        # TODO How hackish is this?
        return self.url(instance) + "leave/"