from django.contrib.auth.models import User
from djangorestframework.resources import ModelResource
from events.models import Game, Event, Publisher, Convention, Demand

class UserResource(ModelResource):
    model = User
    ordering = ('username', )
    fields = ('username', 'first_name', 'last_name')

class PublisherResource(ModelResource):
    model = Publisher
    ordering = ('name', )
    fields = ('id', 'name', 'publisher_url', 'url')

class ConventionResource(ModelResource):
    model = Convention
    ordering = ('name', )
    fields = ('id', 'name')

class GameResource(ModelResource):
    model = Game
    ordering = ('name', )
    fields = ('id', 'name', 'edition', ('publisher', PublisherResource), 'url')

class DemandResource(ModelResource):
    model = Demand
    ordering = ('game', )
    fields = ('id', ('user', UserResource), ('game', GameResource), 'start',
              'end', 'duration', 'url')

class EventResource(ModelResource):
    model = Event
    ordering = ('start', )
    fields = ('id', ('host', UserResource),
              ('players', UserResource),
              ('game', GameResource),
              ('convention', ConventionResource),
              'title', 'start', 'end', 'min', 'max', 'join', 'leave', 'url',
              'duration')
    
    def join(self, instance):
        # TODO How hackish is this?
        return self.url(instance) + "join/"
    
    def leave(self, instance):
        # TODO How hackish is this?
        return self.url(instance) + "leave/"