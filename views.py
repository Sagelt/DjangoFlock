# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseForbidden
from events.models import Publisher, Game, Event, Convention, Demand
from events.forms import PublisherForm, GameForm, ConventionForm, DemandForm, EventForm

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
    return render_to_response('events/list.html', {'events': events}, context_instance=RequestContext(request))

def events_new(request):
    if request.method == 'POST':
        eve = EventForm(request.POST)
        event = eve.save(commit=False)
        event.host = request.user
        event.save()
        return redirect(event)
    return render_to_response('events/new.html', {'form': EventForm()}, context_instance=RequestContext(request))

def events_instance(request, pk):
    event = Event.objects.get(pk=pk)
    return render_to_response('events/instance.html', {'event': event}, context_instance=RequestContext(request))

def events_instance_edit(request, pk):
    event = Event.objects.get(pk=pk)
    if request.method == 'POST':
        eve = EventForm(request.POST, instance=event)
        eve.save()
        return redirect(event)
    return render_to_response('events/edit.html', {'event': event, 'form': EventForm(instance=event)}, context_instance=RequestContext(request))

def events_instance_join(request, pk):
    event = Event.objects.get(pk=pk)
    event.add_player(request.user)
    return redirect(event)

def events_instance_leave(request, pk):
    event = Event.objects.get(pk=pk)
    event.remove_player(request.user)
    return redirect(event)

def demands_list_mine(request):
    if request.user.is_authenticated():
        demands = Demand.objects.filter(user=request.user)
        return render_to_response('demands/list.html', {'object': demands}, context_instance=RequestContext(request))
    return HttpResponseForbidden()

def demands_list(request):
    demands = Demand.objects.all()
    return render_to_response('demands/list.html', {'object': demands}, context_instance=RequestContext(request))

def demands_new(request):
    if request.method == 'POST':
        dem = DemandForm(request.POST)
        demand = dem.save(commit=False)
        demand.user = request.user
        demand.save()
        return redirect(demand)
    return render_to_response('demands/new.html', {'form': DemandForm()}, context_instance=RequestContext(request))

def demands_instance(request, pk):
    demand = Demand.objects.get(pk=pk)
    return render_to_response('demands/instance.html', {'object': demand}, context_instance=RequestContext(request))

def demands_instance_edit(request, pk):
    demand = Demand.objects.get(pk=pk)
    if request.method == 'POST':
        dem = DemandForm(request.POST, instance=demand)
        dem.save()
        return redirect(demand)
    return render_to_response('demands/edit.html', {'object': demand, 'form': DemandForm(instance=demand)}, context_instance=RequestContext(request))
