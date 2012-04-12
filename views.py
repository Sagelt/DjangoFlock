# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from events.models import Publisher, Game, Event

def home(request):
    return render_to_response('base.html')

def register_view(request):
    return render_to_response('signup.html')

def publishers_list(request):
    publishers = Publisher.objects.all()
    return render_to_response('publishers_list.html', {'publishers': publishers})

def publishers_instance(request, pk):
    publisher = Publisher.objects.get(pk=pk)
    return render_to_response('publishers_instance.html', {'publisher': publisher})

def games_list(request):
    games = Game.objects.all()
    return render_to_response('games_list.html', {'games': games})

def games_instance(request, pk):
    game = Game.objects.get(pk=pk)
    return render_to_response('games_instance.html', {'game': game})

def events_list(request):
    events = Event.objects.all()
    return render_to_response('events_list.html', {'events': events})

def events_instance(request, pk):
    event = Event.objects.get(pk=pk)
    return render_to_response('events_instance.html', {'event': event})
