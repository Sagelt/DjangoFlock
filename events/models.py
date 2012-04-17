from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from events.exceptions import EventFullError, OwnEventError

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    publisher_url = models.URLField(blank=True)
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

class Vote(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    start = models.DateTimeField()
    end = models.DateTimeField()
    # @todo: Should this have a Convention foreign key?
    
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
