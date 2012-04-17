"""
These tests aren't very good, yet. Still working on what makes sense to test,
how to deal with database integration tests. Should also write some selenium
tests soon.
"""

from datetime import datetime, timedelta
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.test.client import Client
from events.exceptions import *
from events.models import *
import django.utils.simplejson as json
import time

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
    # This fixture should contain users kit, Test{1-10}
    fixtures = ['events-test.json']
    
    def setUp(self):
        p = Publisher(name='Test Publisher')
        p.save()
        game = Game(name='Test Game', publisher=p)
        game.save()
        host = User.objects.get(username='kit')
        convention = Convention(name='Test Convention')
        convention.save()
        self.event = Event(
            host=host,
            game=game,
            convention=convention,
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
        user = User.objects.get(username='Test10')
        self.assertNotIn(user, self.event.players.all(),
                         "Test precondition failed: Test10 in event already.")
        self.assertRaises(EventFullError, lambda: self.event.add_player(user))
        
    def test_add_player_already_in(self):
        """
        This should be fine, even if the user's already in the event.
        """
        user = User.objects.get(username='Test10')
        self.event.add_player(user)
        self.event.add_player(user)
        self.assertIn(user, self.event.players.all())
    
    def test_add_player(self):
        """
        This should add the user to the event otherwise.
        """
        user = User.objects.get(username='Test10')
        self.event.add_player(user)
        self.assertIn(user, self.event.players.all())
    
    def test_remove_player_already_gone(self):
        """
        This should work fine, even if the user was never a player.
        """
        user = User.objects.get(username='Test10')
        self.assertNotIn(user, self.event.players.all())
        self.event.remove_player(user)
        self.assertNotIn(user, self.event.players.all())
    
    def test_remove_player(self):
        """
        This should work fine, assuming that the player was part of the event
        already.
        """
        user = User.objects.get(username='Test10')
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
        
class ConventionTest(TestCase):
    pass

class DemandTest(TestCase):
    pass

class EventViewTest(TestCase):
    # This fixture should contain users kit, Test{1-10}
    # @todo: This fixture doesn't stress-test these views at all.
    # Work on that.
    fixtures = ['events-test.json']
    
    def setUp(self):
        p = Publisher(name='Test Publisher')
        p.save()
        game = Game(name='Test Game', publisher=p)
        game.save()
        host = User.objects.get(username='kit')
        convention = Convention(name='Test Convention')
        convention.save()
        self.event = Event(
            host=host,
            game=game,
            convention=convention,
            min=3,
            max=5,
            start=datetime.strptime("2012-04-01 11:00", "%Y-%m-%d %H:%M"),
            end=datetime.strptime("2012-04-01 13:00", "%Y-%m-%d %H:%M")
        )
        self.event.save()
    
    def test_filter_start(self):
        start = datetime.strptime("2012-04-01 13:00", "%Y-%m-%d %H:%M")
        start_stamp = int(time.mktime(start.timetuple()))
        response = self.client.get('/api/events/', {'start': start_stamp})
        events = Event.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Event.objects.filter(start__gte=start), map(repr, events))
    
    def test_filter_end(self):
        end = datetime.strptime("2012-04-01 11:00", "%Y-%m-%d %H:%M")
        end_stamp = int(time.mktime(end.timetuple()))
        response = self.client.get('/api/events/', {'end': end_stamp})
        events = Event.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Event.objects.filter(end__lte=end), map(repr, events))
    
    def test_filter_player(self):
        filter = User.objects.filter(username='kit')
        response = self.client.get('/api/events/', {'player': 'kit'})
        events = Event.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Event.objects.filter(players=filter), map(repr, events))
    
    def test_filter_player_list(self):
        filter = User.objects.filter(username__in=['Test1', 'kit'])
        response = self.client.get('/api/events/', {'player': ['Test1', 'kit']})
        events = Event.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Event.objects.filter(players__in=filter), map(repr, events))
    
    def test_filter_host(self):
        filter = User.objects.filter(username='kit')
        response = self.client.get('/api/events/', {'host': 'kit'})
        events = Event.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Event.objects.filter(host=filter), map(repr, events))
    
    def test_filter_host_list(self):
        filter = User.objects.filter(username__in=['Test1', 'kit'])
        response = self.client.get('/api/events/', {'host': ['Test1', 'kit']})
        events = Event.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Event.objects.filter(host__in=filter), map(repr, events))
    
    def test_unfiltered(self):
        response = self.client.get('/api/events/')
        events = Event.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Event.objects.filter(), map(repr, events))

class DemandViewTest(TestCase):
    # This fixture should contain users kit, Test{1-10}
    # @todo: This fixture doesn't stress-test these views at all.
    # Work on that.
    fixtures = ['events-test.json']
    
    def setUp(self):
        user = User.objects.get(username='kit')
        game = Game.objects.get(id=1)
        demand = Demand(
            start=datetime.strptime("2012-04-01 11:00", "%Y-%m-%d %H:%M"),
            end=datetime.strptime("2012-04-01 20:00", "%Y-%m-%d %H:%M"),
            game=game,
            user=user
        )
        demand.save()
    
    def test_unfiltered(self):
        response = self.client.get('/api/demands/')
        demands = Demand.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Demand.objects.filter(), map(repr, demands))
    
    def test_filter_start(self):
        start = datetime.strptime("2012-04-01 13:00", "%Y-%m-%d %H:%M")
        start_stamp = int(time.mktime(start.timetuple()))
        response = self.client.get('/api/demands/', {'start': start_stamp})
        demands = Demand.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Demand.objects.filter(end__gte=start), map(repr, demands))
    
    def test_filter_end(self):
        end = datetime.strptime("2012-04-01 13:00", "%Y-%m-%d %H:%M")
        end_stamp = int(time.mktime(end.timetuple()))
        response = self.client.get('/api/demands/', {'end': end_stamp})
        demands = Demand.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Demand.objects.filter(start__lte=end), map(repr, demands))
    
    def test_filter_game(self):
        filter = Game.objects.get(id=1)
        response = self.client.get('/api/demands/', {'game': 1})
        demands = Demand.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Demand.objects.filter(game=filter), map(repr, demands))
    
    def test_filter_game_list(self):
        filter = Game.objects.get(id__in=[1, 2])
        response = self.client.get('/api/demands/', {'game': [1, 2]})
        demands = Demand.objects.filter(id__in=[x['id'] for x in json.loads(response.content)])
        self.assertQuerysetEqual(Demand.objects.filter(game=filter), map(repr, demands))
