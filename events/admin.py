from django.contrib import admin
from events.models import Game, Event, Publisher, Convention, Demand

admin.site.register(Game)
admin.site.register(Event)
admin.site.register(Publisher)
admin.site.register(Convention)
admin.site.register(Demand)