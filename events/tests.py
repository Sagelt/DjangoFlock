"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
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
        self.assertQuerysetEqual(Game.objects.filter(name='Fiasco'), ['<Game: Fiasco>'])
    
    def test_list(self):
        pass
    
    def test_retrieve(self):
        pass
    
    def test_update(self):
        pass
    
    def test_delete(self):
        pass

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
