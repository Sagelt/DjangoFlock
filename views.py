# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from events.models import Publisher, Game, Event

def home(request):
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('base.html')

def register_view(request):
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('signup.html')

def publishers_list(request):
    publishers = Publisher.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('publishers_list.html', {'publishers': publishers})

def publishers_new(request):
    publishers = Publisher.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('publishers_list.html', {'publishers': publishers})

def publishers_instance(request, pk):
    publisher = Publisher.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('publishers_instance.html', {'publisher': publisher})

def publishers_instance_edit(request, pk):
    publisher = Publisher.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('publishers_instance.html', {'publisher': publisher})

def games_list(request):
    games = Game.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('games_list.html', {'games': games})

def games_new(request):
    games = Game.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('games_list.html', {'games': games})

def games_instance(request, pk):
    game = Game.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('games_instance.html', {'game': game})

def games_instance_edit(request, pk):
    game = Game.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('games_instance.html', {'game': game})

def conventions_list(request):
    raise NotImplementedError

def conventions_new(request):
    raise NotImplementedError

def conventions_instance(request, pk):
    raise NotImplementedError

def conventions_instance_edit(request, pk):
    raise NotImplementedError

def events_list(request):
    events = Event.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_list.html', {'events': events})

def events_new(request):
    events = Event.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_list.html', {'events': events})

def events_instance(request, pk):
    event = Event.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_instance.html', {'event': event})

def events_instance_edit(request, pk):
    event = Event.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_instance.html', {'event': event})

def events_instance_join(request, pk):
    event = Event.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_instance.html', {'event': event})

def events_instance_leave(request, pk):
    event = Event.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_instance.html', {'event': event})

def demands_list(request):
    raise NotImplentedError

def demands_list_mine(request):
    raise NotImplentedError

def demands_new(request):
    raise NotImplentedError

def demands_instance(request, pk):
    raise NotImplentedError

def demands_instance_edit(request, pk):
    raise NotImplentedError
