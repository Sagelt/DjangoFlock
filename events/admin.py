from django.contrib import admin
from events.models import Game, Event, Publisher

admin.site.register(Game)
admin.site.register(Event)
admin.site.register(Publisher)