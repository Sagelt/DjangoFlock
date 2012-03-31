"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

These tests aren't very good, yet. Still working on what makes sense to test,
how to deal with database integration tests. Should also write some selenium
tests soon.
"""

from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from events.models import *


class GameTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('kit', 'kit.la.t@gmail.com', 'foobar')
        User.objects.create_user('blasto', 'blasto@example.com', 'foobar')
        Publisher(name='Bully Pulpit').save()
    
    def tearDown(self):
        pass
    
    def test_login(self):
        assert self.client.login(username='kitx', password='foobar') is False
        assert self.client.login(username='kit', password='foobar') is True
    
    def test_create(self):
        # not logged in:
        response = self.client.post('/games/', {'name': 'Fiasco', 'publisher': 1})
        assert response.status_code == 403
        assert len(Game.objects.all()) == 0
        # logged in but with bad data:
        self.client.login(username='kit', password='foobar')
        response = self.client.post('/games/', {'namex': 'Fiasco', 'publisher': 1})
        assert response.status_code == 400
        assert len(Game.objects.all()) == 0
        # logged in and with good data
        response = self.client.post('/games/', {'name': 'Fiasco', 'publisher': 1})
        assert response.status_code == 201
        self.assertQuerysetEqual(Game.objects.filter(name='Fiasco'),
                                 ['Fiasco'], lambda m: m.name)
    
    def test_list(self):
        response = self.client.get('/games/',
                                   **{'Accept': 'application/json',
                                      'CONTENT_TYPE': 'application/json'})
        assert response.status_code == 200
        # TODO some assertion that there are an appropriate n items in the
        # response. Should probably get plaintext or json response, then.
        # Unclear why the code above isn't getting a json response.
        #assert
    
    def test_retrieve(self):
        publisher = Publisher.objects.get(name='Bully Pulpit')
        Game(name='Fiasco', publisher=publisher).save()
        response = self.client.get('/games/1/')
        assert response.status_code == 200
    
    def test_update(self):
        publisher = Publisher.objects.get(name='Bully Pulpit')
        Game(name='Fiasco', publisher=publisher).save()
        # Not logged in
        response = self.client.put('/games/1/', {'name': 'Fiascox', 'publisher': publisher.id})
        assert response.status_code == 403
        assert len(Game.objects.filter(name='Fiascox')) == 0
        # Logged in
        self.client.login(username='kit', password='foobar')
        response = self.client.put('/games/1/', {'name': 'Fiascox', 'publisher': publisher.id})
        assert response.status_code == 200
        assert len(Game.objects.filter(name='Fiascox')) == 1
    
    def test_delete(self):
        publisher = Publisher.objects.get(name='Bully Pulpit')
        Game(name='Fiasco', publisher=publisher).save()
        # Not logged in
        response = self.client.delete('/games/1/')
        assert response.status_code == 403
        assert len(Game.objects.filter(name='Fiasco')) == 1
        # Logged in
        self.client.login(username='kit', password='foobar')
        response = self.client.delete('/games/1/')
        # TODO This should be returning a 204, right? Or am I crazy?
        assert response.status_code == 204
        assert len(Game.objects.filter(name='Fiasco')) == 0

class EventTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('kit', 'kit.la.t@gmail.com', 'foobar')
        User.objects.create_user('blasto', 'blasto@example.com', 'foobar')
        publisher = Publisher(name='Bully Pulpit')
        publisher.save()
        Game(name='Fiasco', publisher=publisher).save()
    
    def tearDown(self):
        pass
    
    def test_create(self):
        # Not logged in
        response = self.client.post('/events/', {
            'game': 1,
            'start': '2012-03-29 14:00',
            'end': '2012-03-29 16:00',
            'min': 3,
            'max': 5
        })
        assert response.status_code == 403
        assert len(Event.objects.all()) == 0
        # logged in but with bad data
        self.client.login(username='kit', password='foobar')
        response = self.client.post('/events/', {
            'game': 2, # There shouldn't be a Game with ID 2 at this point.
            'start': '2012-03-29 14:00',
            'end': '2012-03-29 16:00',
            'min': 3,
            'max': 5
        })
        assert response.status_code == 400
        assert len(Event.objects.all()) == 0
        # logged in and with good data
        response = self.client.post('/events/', {
            'game': 1,
            'start': '2012-03-29 14:00',
            'end': '2012-03-29 16:00',
            'min': 3,
            'max': 5
        })
        assert response.status_code == 201
        assert len(Event.objects.all()) == 1
    
    def test_list(self):
        response = self.client.get('/events/',
                                   **{'Accept': 'application/json'})
        assert response.status_code == 200
        # TODO some assertion that there are an appropriate n items in the
        # response.
    
    def test_retrieve(self):
        game = Game.objects.get(name='Fiasco')
        event = Event(
            game=game,
            start=datetime.strptime("2012-03-29 14:00", "%Y-%m-%d %H:%M"),
            end=datetime.strptime("2012-03-29 16:00", "%Y-%m-%d %H:%M"),
            min=3,
            max=5,
            host=User.objects.get(username='kit')
        )
        event.save()
        response = self.client.get('/events/%s/' % event.id)
        assert response.status_code == 200
    
    def test_update(self):
        game = Game.objects.get(name='Fiasco')
        event = Event(
            game=game,
            start=datetime.strptime("2012-03-29 14:00", "%Y-%m-%d %H:%M"),
            end=datetime.strptime("2012-03-29 16:00", "%Y-%m-%d %H:%M"),
            min=3,
            max=5,
            host=User.objects.get(username='kit')
        )
        event.save()
        # Not logged in
        response = self.client.put('/events/%s/' % event.id, dict(
            game=game.id,
            start='2012-03-29 14:00',
            end='2012-03-29 16:00',
            min=4,
            max=5,
        ))
        assert response.status_code == 403
        assert Event.objects.get(id=event.id).min == 3
        # Logged in as wrong user
        self.client.login(username='blasto', password='foobar')
        response = self.client.put('/events/%s/' % event.id, dict(
            game=game.id,
            start='2012-03-29 14:00',
            end='2012-03-29 16:00',
            min=4,
            max=5,
        ))
        assert response.status_code == 403
        assert Event.objects.get(id=event.id).min == 3
        # Logged in as right user, bad data
        self.client.logout()
        self.client.login(username='kit', password='foobar')
        response = self.client.put('/events/%s/' % event.id, dict(
            game=game.id,
            start='2012-03-29 14:00',
            end='2012-03-29 16:00',
            min='what?',
            max=5,
        ))
        assert response.status_code == 400
        assert Event.objects.get(id=event.id).min == 3
        # Logged in as right user, good data
        response = self.client.put('/events/%s/' % event.id, dict(
            game=game.id,
            start='2012-03-29 14:00',
            end='2012-03-29 16:00',
            min=4,
            max=5,
        ))
        assert response.status_code == 200
        assert Event.objects.get(id=event.id).min == 4
    
    def test_delete(self):
        pass
