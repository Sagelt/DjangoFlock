from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from events.exceptions import EventFullException, OwnEventException

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Event(models.Model):
    host = models.ForeignKey(User, related_name='host')
    players = models.ManyToManyField(User, blank=True, null=True)
    game = models.ForeignKey(Game)
    start = models.DateTimeField()
    end = models.DateTimeField()
    min = models.IntegerField()
    max = models.IntegerField()
    
    def add_player(self, user):
        """
        If you are already in the event, no problem.
        If you are the host or the event is full or you are not authenticated,
        then you get a bad response.
        """
        if not user.is_authenticated():
            raise ValueError
        if user == self.host:
            raise OwnEventException
        if len(self.players.all()) >= self.max:
            raise EventFullException
        if user in self.players.all():
            return
        self.players.add(user)
        self.save()
    
    def remove_player(self, user):
        """
        This method is idempotent; there's no problem with removing a user who's not present.
        """
        self.players.remove(user)
        self.save()
    
    def is_ready(self):
        return len(self.players.all()) >= self.min
    
    def is_ongoing(self):
        return self.start <= datetime.now() <= self.end
    
    @property
    def duration(self):
        return self.end - self.start
