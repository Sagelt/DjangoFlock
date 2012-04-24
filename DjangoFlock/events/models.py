from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from events.exceptions import EventFullError, OwnEventError
from textwrap import dedent

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=50, unique=True)
    publisher_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return "/publishers/%s/" % self.id

class Game(models.Model):
    name = models.CharField(max_length=50)
    edition = models.CharField(max_length=50, blank=True)
    publisher = models.ForeignKey(Publisher)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return "/games/%s/" % self.id

class Convention(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return "/conventions/%s/" % self.id

class Event(models.Model):
    host = models.ForeignKey(User, related_name='host')
    players = models.ManyToManyField(User, blank=True, null=True)
    game = models.ForeignKey(Game)
    convention = models.ForeignKey(Convention)
    start = models.DateTimeField()
    end = models.DateTimeField()
    min = models.IntegerField()
    max = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def add_player(self, user):
        """
        If you are already in the event, no problem.
        If you are the host or the event is full or you are not authenticated,
        then you get a bad response.
        """
        if not user.is_authenticated():
            raise ValueError
        if user == self.host:
            raise OwnEventError
        if len(self.players.all()) >= self.max:
            raise EventFullError
        if user in self.players.all():
            return
        self.players.add(user)
        self.save()
    
    def remove_player(self, user):
        """
        This method is idempotent; there's no problem with removing a user
        who's not present.
        """
        self.players.remove(user)
        self.save()
    
    def is_ready(self):
        return len(self.players.all()) >= self.min
    
    def is_ongoing(self):
        return self.start <= datetime.now() <= self.end
    
    @property
    def duration(self):
        """
        This used to return a timedelta. Now it returns a float of the number
        of hours of the event.
        
        Timedelta objects store days and seconds, so you have to take the
        seconds and divide by 60 * 60.
        """
        return (self.end - self.start).seconds / float(60 * 60)
    
    @property
    def title(self):
        return "%s with %s" % (self.game.name, self.host.username)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.id)
    
    def get_absolute_url(self):
        return "/events/%s/" % self.id 

class Demand(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    start = models.DateTimeField()
    end = models.DateTimeField()
    convention = models.ForeignKey(Convention)
    
    @property
    def duration(self):
        """
        This used to return a timedelta. Now it returns a float of the number
        of hours of the event.
        
        Timedelta objects store days and seconds, so you have to take the
        seconds and divide by 60 * 60.
        """
        return (self.end - self.start).seconds / float(60 * 60)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.id)
    
    def get_absolute_url(self):
        return "/demands/%s/" % self.id

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    active_convention = models.ForeignKey(Convention, blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return "User Profile: %s" % self.user.username

# Signals
def notify_interested_users(sender, instance, created, **kwargs):
    relevant_demands = Demand.objects.filter(
        game=instance.game,
        start__lte=instance.start,
        end__gte=instance.end
    #).exclude(
    #    user=instance.host
    )
    current_site = Site.objects.get_current()
    domain = current_site.domain
    for demand in relevant_demands:
        email = demand.user.email
        if email:
            send_mail(
                '[RPGflock] New Event!',
                dedent("""\
                There's a new event on RPGflock you may be interested in:
                
                %(title)s.
                
                To check it out, just go to http://%(domain)s%(url)s.
                """ % {'title': instance.title,
                       'domain': domain,
                       'url': instance.get_absolute_url()}),
                'no-reply@rpgflock.com',
                [email],
                fail_silently=False
            )
# Send the notifications. Just email for now.
# This signal is getting sent twice. Why?
post_save.connect(notify_interested_users, sender=Event, dispatch_uid='notify_interested_users')

# Register a callback function to create a user profile if none present.
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Shenanigans here.
        # Because Django REST Framework assumes that an InstanceModelView uses a
        # Model, not a resource, it can't deal with a resource that flattens out
        # two models with a one-to-one relationship. This is a hackish way of
        # getting around it. I specify the fields in the UserProfile, and take
        # them off of the User, where DRF has put them, and stick them back on
        # the profile where they go. Then I throw up in my mouth a little.
        # So very not DRY.
        profile_fields = ('active_convention', )
        profile = instance.get_profile()
        for field in profile_fields:
            val = getattr(instance, field, None)
            setattr(profile, field, val)
        profile.save()
post_save.connect(create_or_save_user_profile, sender=User, dispatch_uid='create_or_save_user_profile')
