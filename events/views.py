# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from events.models import Game, Event

def list_games(request):
    games = Game.objects.all().order_by('name')
    return render_to_response('events/game_list.html', {'games': games})

def create_game_form(request):
    pass

def retrieve_game(request, id):
    game = get_object_or_404(Game, pk=id)
    return render_to_response('events/game.html', {'game': game})

def edit_game_form(request):
    pass

def delete_game_form(request):
    pass