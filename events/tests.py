"""
These tests aren't very good, yet. Still working on what makes sense to test,
how to deal with database integration tests. Should also write some selenium
tests soon.
"""

from datetime import datetime, timedelta
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.test.client import Client
from events.models import *
from events.exceptions import *

class PublisherTest(TestCase):
    """
    Publisher models have no methods. Not much to test here! 
    """
    pass

class GameTest(TestCase):
    """
    Game models have no methods. Not much to test here! 
    """
    pass

class EventTest(TestCase):
    """
    Event models have four methods, without significant interactions.
    """
    fixtures = ['events-test.json']
    
    def setUp(self):
        p = Publisher(name='Test Publisher')
        p.save()
        game = Game(name='Test Game', publisher=p)
        game.save()
        host = User.objects.get(username='kit')
        self.event = Event(
            host=host,
            game=game,
            min=3,
            max=5,
            start=datetime.strptime("2012-04-01 11:00", "%Y-%m-%d %H:%M"),
            end=datetime.strptime("2012-04-01 13:00", "%Y-%m-%d %H:%M")
        )
        self.event.save()
    
    def test_add_player_not_authenticated(self):
        """
        This should throw a ValueError if the user is not authenticated.
        """
        user = AnonymousUser()
        self.assertRaises(ValueError, lambda: self.event.add_player(user))
        
    def test_add_player_is_host(self):
        """
        This should throw an OwnEventError if the user is the host.
        """
        user = self.event.host
        self.assertRaises(OwnEventError, lambda: self.event.add_player(user))
        
    def test_add_player_event_full(self):
        """
        This should throw an EventFullError if the event has no free slots.
        """
        # Make sure that the event is full. There are test users from Test1 to
        # Test10 in the fixture.
        for i in range(len(self.event.players.all()), self.event.max):
            user = User.objects.get(username='Test%s' % (i + 1))
            self.event.add_player(user)
        user = User.objects.get(username='blasto')
        self.assertRaises(EventFullError, lambda: self.event.add_player(user))
        
    def test_add_player_already_in(self):
        """
        This should be fine, even if the user's already in the event.
        """
        user = User.objects.get(username='blasto')
        self.event.add_player(user)
        self.event.add_player(user)
        self.assertIn(user, self.event.players.all())
    
    def test_add_player(self):
        """
        This should add the user to the event otherwise.
        """
        user = User.objects.get(username='blasto')
        self.event.add_player(user)
        self.assertIn(user, self.event.players.all())
    
    def test_remove_player_already_gone(self):
        """
        This should work fine, even if the user was never a player.
        """
        user = User.objects.get(username='blasto')
        self.assertNotIn(user, self.event.players.all())
        self.event.remove_player(user)
        self.assertNotIn(user, self.event.players.all())
    
    def test_remove_player(self):
        """
        This should work fine, assuming that the player was part of the event
        already.
        """
        user = User.objects.get(username='blasto')
        self.event.add_player(user)
        self.assertIn(user, self.event.players.all())
        self.event.remove_player(user)
        self.assertNotIn(user, self.event.players.all())
    
    def test_is_ready_underfull(self):
        """
        This should be false.
        """
        self.assertLess(len(self.event.players.all()), self.event.min)
        self.assertFalse(self.event.is_ready())
    
    def test_is_ready(self):
        """
        This should be true.
        """
        self.assertLess(len(self.event.players.all()), self.event.min)
        # Add players until you reach the min.
        for i in range(len(self.event.players.all()), self.event.min):
            user = User.objects.get(username='Test%s' % (i + 1))
            self.event.add_player(user)
        self.assertTrue(self.event.is_ready())
    
    def test_is_ongoing_not_yet(self):
        """
        Make the event's dates in the future.
        """
        now = datetime.now()
        start_delta = timedelta(hours=1)
        end_delta = timedelta(hours=2)
        self.event.start = now + start_delta
        self.event.end = now + end_delta
        self.event.save()
        self.assertFalse(self.event.is_ongoing())
    
    def test_is_ongoing_already_past(self):
        """
        Make the event's dates in the past.
        """
        now = datetime.now()
        start_delta = timedelta(hours=-2)
        end_delta = timedelta(hours=-1)
        self.event.start = now + start_delta
        self.event.end = now + end_delta
        self.event.save()
        self.assertFalse(self.event.is_ongoing())
    
    def test_is_ongoing(self):
        """
        Make the event's dates on either side of now.
        """
        now = datetime.now()
        start_delta = timedelta(hours=-1)
        end_delta = timedelta(hours=1)
        self.event.start = now + start_delta
        self.event.end = now + end_delta
        self.event.save()
        self.assertTrue(self.event.is_ongoing())
