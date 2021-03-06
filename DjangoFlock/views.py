# Create your views here.
from collections import namedtuple
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from events.forms import (PublisherForm, GameForm, ConventionForm, DemandForm, 
    EventForm, DemandFilterForm)
from events.models import Publisher, Game, Event, Convention, Demand
from events.utils import datetime_range
import urllib

def home(request):
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('base.html', context_instance=RequestContext(request))

def register_view(request):
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('signup.html', context_instance=RequestContext(request))

def users_list(request):
    users = User.objects.order_by('username')
    return render_to_response('users/list.html',
                              {'user_list': users},
                              context_instance=RequestContext(request))

def users_instance(request, username):
    user = get_object_or_404(User, username=username)
    return render_to_response('users/instance.html',
                              {'user_instance': user},
                              context_instance=RequestContext(request))

# ======== Flock-related views. Should refactor and make more generic

def publishers_list(request):
    publishers = Publisher.objects.all()
    if request.flavour == 'mobile':
        return render_to_response("mobile/mobile.html")
    return render_to_response('publishers/list.html', {'object': publishers}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def publishers_new(request):
    if request.is_ajax():
        render_target = '_form.html'
    else:
        render_target = 'new.html'
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            return redirect(publisher)
    else:
        form = PublisherForm()
    return render_to_response('publishers/%s' % render_target,
                              {'form': form, 'editing': False},
                              context_instance=RequestContext(request))

def publishers_instance(request, pk):
    publisher = Publisher.objects.get(pk=pk)
    return render_to_response('publishers/instance.html', {'object': publisher}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def publishers_instance_edit(request, pk):
    publisher = Publisher.objects.get(pk=pk)
    if request.is_ajax():
        render_target = '_form.html'
    else:
        render_target = 'edit.html'
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect(publisher)
    else:
        form = PublisherForm(instance=publisher)
    return render_to_response('publishers/%s' % render_target,
                              {'object': publisher,
                               'form': form,
                               'editing': True},
                              context_instance=RequestContext(request))

def games_list(request):
    games = Game.objects.all()
    return render_to_response('games/list.html', {'object': games}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def games_new(request):
    if request.is_ajax():
        render_target = '_form.html'
    else:
        render_target = 'new.html'
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save()
            return redirect(game)
    else:
        form = GameForm()
    return render_to_response('games/%s' % render_target,
                              {'form': form, 'editing': False},
                              context_instance=RequestContext(request))

def games_instance(request, pk):
    game = Game.objects.get(pk=pk)
    return render_to_response('games/instance.html', {'object': game}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def games_instance_edit(request, pk):
    game = Game.objects.get(pk=pk)
    if request.is_ajax():
        render_target = '_form.html'
    else:
        render_target = 'edit.html'
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect(game)
    else:
        form = GameForm(instance=game)
    return render_to_response('games/%s' % render_target,
                              {'object': game,
                               'form': form,
                               'editing': True},
                              context_instance=RequestContext(request))

def events_list(request):
    # @todo: Rather than replicate code, make this page make an async call to
    # the REST API. But what if you have no JS? Then this will be the fallback
    kwargs = {}
    if request.user.is_authenticated() and request.user.get_profile().active_convention is not None:
        kwargs['convention'] = request.user.get_profile().active_convention
    events = Event.objects.filter(**kwargs)
    return render_to_response('events/list.html', {'events': events}, context_instance=RequestContext(request))

@login_required
def events_new(request):
    if request.is_ajax():
        render_target = '_form.html'
    else:
        render_target = 'new.html'
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            return redirect(event)
    else:
        form = EventForm(initial=request.GET.dict())
    return render_to_response('events/%s' % render_target,
                              {'form': form, 'editing': False},
                              context_instance=RequestContext(request))

def events_instance(request, pk):
    event = Event.objects.get(pk=pk)
    return render_to_response('events/instance.html', {'event': event}, context_instance=RequestContext(request))

@login_required
def events_instance_edit(request, pk):
    event = Event.objects.get(pk=pk)
    if request.is_ajax():
        render_target = '_form.html'
    else:
        render_target = 'edit.html'
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save(commit=False)
            return redirect(event)
    else:
        form = EventForm(instance=event)
    return render_to_response('events/%s' % render_target,
                              {'object': event,
                               'form': form,
                               'editing': True},
                              context_instance=RequestContext(request))

@login_required
def events_instance_join(request, pk):
    event = Event.objects.get(pk=pk)
    event.add_player(request.user)
    return redirect(event)

@login_required
def events_instance_leave(request, pk):
    event = Event.objects.get(pk=pk)
    event.remove_player(request.user)
    return redirect(event)

# ==================
# TODO Refactor views from here down.

def conventions_list(request):
    conventions = Convention.objects.all()
    return render_to_response('conventions/list.html', {'object': conventions}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def conventions_new(request):
    if request.method == 'POST':
        con = ConventionForm(request.POST)
        convention = con.save()
        return redirect(convention)
    return render_to_response('conventions/new.html', {'form': ConventionForm()}, context_instance=RequestContext(request))

def conventions_instance(request, pk):
    convention = Convention.objects.get(pk=pk)
    return render_to_response('conventions/instance.html', {'object': convention}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def conventions_instance_edit(request, pk):
    convention = Convention.objects.get(pk=pk)
    if request.method == 'POST':
        con = ConventionForm(request.POST, instance=convention)
        con.save()
        return redirect(convention)
    return render_to_response('conventions/edit.html', {'object': convention, 'form': ConventionForm(instance=convention)}, context_instance=RequestContext(request))

@login_required
def demands_list_mine(request):
    if request.user.is_authenticated():
        demands = Demand.objects.filter(user=request.user)
        return render_to_response('demands/list.html', {'object': demands}, context_instance=RequestContext(request))
    return HttpResponseForbidden()

@csrf_exempt
def demands_list(request):
    # @todo: Rather than replicate code, make this page make an async call to
    # the REST API. But what if you have no JS? Then this will be the fallback.
    kwargs = {}
    filter_form = DemandFilterForm(request.GET)
    if request.GET.get('games') and filter_form.is_valid():
        kwargs['game__in'] = filter_form.cleaned_data['games']
    if request.user.is_authenticated() and request.user.get_profile().active_convention is not None:
        kwargs['convention'] = request.user.get_profile().active_convention
    demands = Demand.objects.filter(**kwargs)
    # From start to end, make half-hour slots for every half-hour that has any
    # demand in it.
    # In each slot, put the count of demand-per-game.
    # Return [(slot_start, slot_end, [node, ...]), ...]
    if request.GET.get('start') and filter_form.is_valid():
        #start = datetime.fromtimestamp(int(request.GET['start']))
        start = filter_form.cleaned_data['start']
    else:
        start = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    if request.GET.get('end') and filter_form.is_valid():
        #end = datetime.fromtimestamp(int(request.GET['end']))
        end = filter_form.cleaned_data['end']
    else:
        if demands:
            end = max(d.end for d in demands)
        else:
            #end = datetime.max
            end = start + timedelta(hours=24)
    results = []
    Node = namedtuple('Node', ("game", "url", "votes"))
    # @bug: datetime_range, while a generator, can still take a huge lot of time
    # and beat the database with a stick if the span between start and end is
    # too large. Hand-check?
    for slot_start, slot_end in datetime_range(start, end):
        votes = demands.filter(start__lte=slot_end, end__gte=slot_start).values('game__id', 'game__name').annotate(Count('game__name'))
        slot = [slot_start, slot_end, []]
        for vote in votes:
            node = Node(
                vote['game__name'],
                reverse('events-new') + '?' + urllib.urlencode({
                    'game': vote['game__id'],
                    'start': slot_start,
                    'end': slot_end
                }),
                vote['game__name__count']
            )
            slot[2].append(node)
        results.append(tuple(slot))
    demand_filter_form = DemandFilterForm(request.GET)
    return render_to_response('demands/list.html',
        {'object': demands,
        'results': results,
        'filter_form': demand_filter_form},
        context_instance=RequestContext(request))

@login_required
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

@login_required
def demands_instance_edit(request, pk):
    demand = Demand.objects.get(pk=pk)
    if request.user != demand.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        dem = DemandForm(request.POST, instance=demand)
        dem.save()
        return redirect(demand)
    return render_to_response('demands/edit.html', {'object': demand, 'form': DemandForm(instance=demand)}, context_instance=RequestContext(request))
