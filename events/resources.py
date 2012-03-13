from djangorestframework.resources import ModelResource
from events.models import Game, Event

class GameResource(ModelResource):
    model = Game
    
class EventResource(ModelResource):
    model = Event

