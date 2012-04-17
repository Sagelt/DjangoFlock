# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from events.models import Publisher, Game, Event, Convention
from events.forms import PublisherForm, GameForm, ConventionForm

def home(request):
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('base.html', context_instance=RequestContext(request))

def register_view(request):
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('signup.html', context_instance=RequestContext(request))

def publishers_list(request):
    publishers = Publisher.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('publishers/list.html', {'object': publishers}, context_instance=RequestContext(request))

def publishers_new(request):
    if request.method == 'POST':
        pub = PublisherForm(request.POST)
        publisher = pub.save()
        return redirect(publisher)
    return render_to_response('publishers/new.html', {'form': PublisherForm()}, context_instance=RequestContext(request))

def publishers_instance(request, pk):
    publisher = Publisher.objects.get(pk=pk)
    return render_to_response('publishers/instance.html', {'object': publisher}, context_instance=RequestContext(request))

def publishers_instance_edit(request, pk):
    publisher = Publisher.objects.get(pk=pk)
    if request.method == 'POST':
        pub = PublisherForm(request.POST, instance=publisher)
        pub.save()
        return redirect(publisher)
    return render_to_response('publishers/edit.html', {'object': publisher, 'form': PublisherForm(instance=publisher)}, context_instance=RequestContext(request))

def games_list(request):
    games = Game.objects.all()
    return render_to_response('games/list.html', {'object': games}, context_instance=RequestContext(request))

def games_new(request):
    if request.method == 'POST':
        gam = GameForm(request.POST)
        game = gam.save()
        return redirect(game)
    return render_to_response('games/new.html', {'form': GameForm()}, context_instance=RequestContext(request))

def games_instance(request, pk):
    game = Game.objects.get(pk=pk)
    return render_to_response('games/instance.html', {'object': game}, context_instance=RequestContext(request))

def games_instance_edit(request, pk):
    game = Game.objects.get(pk=pk)
    if request.method == 'POST':
        gam = GameForm(request.POST, instance=game)
        gam.save()
        return redirect(game)
    return render_to_response('games/edit.html', {'object': game, 'form': GameForm(instance=game)}, context_instance=RequestContext(request))

def conventions_list(request):
    conventions = Convention.objects.all()
    return render_to_response('conventions/list.html', {'object': conventions}, context_instance=RequestContext(request))

def conventions_new(request):
    if request.method == 'POST':
        con = ConventionForm(request.POST)
        convention = con.save()
        return redirect(convention)
    return render_to_response('conventions/new.html', {'form': ConventionForm()}, context_instance=RequestContext(request))

def conventions_instance(request, pk):
    convention = Convention.objects.get(pk=pk)
    return render_to_response('conventions/instance.html', {'object': convention}, context_instance=RequestContext(request))

def conventions_instance_edit(request, pk):
    convention = Convention.objects.get(pk=pk)
    if request.method == 'POST':
        con = ConventionForm(request.POST, instance=convention)
        con.save()
        return redirect(convention)
    return render_to_response('conventions/edit.html', {'object': convention, 'form': ConventionForm(instance=convention)}, context_instance=RequestContext(request))

def events_list(request):
    events = Event.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_list.html', {'events': events}, context_instance=RequestContext(request))

def events_new(request):
    events = Event.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_list.html', {'events': events}, context_instance=RequestContext(request))

def events_instance(request, pk):
    event = Event.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_instance.html', {'event': event}, context_instance=RequestContext(request))

def events_instance_edit(request, pk):
    event = Event.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_instance.html', {'event': event}, context_instance=RequestContext(request))

def events_instance_join(request, pk):
    event = Event.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_instance.html', {'event': event}, context_instance=RequestContext(request))

def events_instance_leave(request, pk):
    event = Event.objects.get(pk=pk)
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('events_instance.html', {'event': event}, context_instance=RequestContext(request))

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
