from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Event(models.Model):
    gm = models.ForeignKey(User, related_name='gm')
    players = models.ManyToManyField(User, blank=True, null=True)
    game = models.ForeignKey(Game)
    start = models.DateTimeField()
    end = models.DateTimeField()
    min = models.IntegerField()
    max = models.IntegerField()
    
    def add_player(self, user):
        if user not in self.players and len(self.players) < self.max:
            self.players.add(user)
            return True
        return False
    
    def remove_player(self, user):
        self.players.remove(user)
    
    def is_ready(self):
        return len(self.players) >= self.min
    
    def is_ongoing(self):
        return self.start <= datetime.now() <= self.end
    
    @property
    def duration(self):
        return self.end - self.start