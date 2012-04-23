from django.contrib import admin
from events.models import Game, Event, Publisher, Convention, Demand

admin.site.register(Game)
admin.site.register(Event)
admin.site.register(Publisher)
admin.site.register(Convention)
admin.site.register(Demand)

# Show user profiles inline in the Django Admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from events.models import UserProfile
 
admin.site.unregister(User)
 
class UserProfileInline(admin.StackedInline):
    model = UserProfile
 
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
 
admin.site.register(User, UserProfileAdmin)
