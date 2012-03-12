from django.db import models
from datetime import datetime

# Create your models here.

class Game(models.Model):
    name = models.StringField()

class Event(models.Model):
    gm = models.ForeignKey(models.User)
    players = models.ManyToManyField(models.User)
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