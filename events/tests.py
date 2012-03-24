"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

These tests aren't very good, yet. Still working on what makes sense to test,
how to deal with database integration tests. Should also write some selenium
tests soon.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from events.models import *

class GameTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('kit', 'kit.la.t@gmail.com', 'foobar')
        User.objects.create_user('blasto', 'blasto@example.com', 'foobar')
    
    def tearDown(self):
        pass
    
    def test_login(self):
        assert self.client.login(username='kitx', password='foobar') is False
        assert self.client.login(username='kit', password='foobar') is True
    
    def test_create(self):
        # not logged in:
        response = self.client.post('/games/', {'name': 'Fiasco'})
        assert response.status_code == 403
        assert len(Game.objects.all()) == 0
        # logged in but with bad data:
        self.client.login(username='kit', password='foobar')
        response = self.client.post('/games/', {'namex': 'Fiasco'})
        assert response.status_code == 400
        assert len(Game.objects.all()) == 0
        # logged in and with good data
        response = self.client.post('/games/', {'name': 'Fiasco'})
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
        Game(name='Fiasco').save()
        response = self.client.get('/games/1/')
        assert response.status_code == 200
    
    def test_update(self):
        Game(name='Fiasco').save()
        # Not logged in
        response = self.client.put('/games/1/', {'name': 'Fiascox'})
        assert response.status_code == 403
        assert len(Game.objects.filter(name='Fiascox')) == 0
        # Logged in
        self.client.login(username='kit', password='foobar')
        response = self.client.put('/games/1/', {'name': 'Fiascox'})
        assert response.status_code == 200
        assert len(Game.objects.filter(name='Fiascox')) == 1
    
    def test_delete(self):
        Game(name='Fiasco').save()
        # Not logged in
        response = self.client.delete('/games/1/')
        assert response.status_code == 403
        assert len(Game.objects.filter(name='Fiasco')) == 1
        # Logged in
        self.client.login(username='kit', password='foobar')
        response = self.client.delete('/games/1/')
        assert response.status_code == 204
        assert len(Game.objects.filter(name='Fiasco')) == 0

class EventTest(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_create(self):
        pass
    
    def test_list(self):
        pass
    
    def test_retrieve(self):
        pass
    
    def test_update(self):
        pass
    
    def test_delete(self):
        pass
