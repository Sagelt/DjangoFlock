from django.conf.urls import patterns, include, url
from djangorestframework.permissions import IsUserOrIsAnonReadOnly
from djangorestframework.views import InstanceModelView, ListOrCreateModelView
from events.resources import GameResource, EventResource, PublisherResource
from events.views import EventRoot, EventModelView, GameRoot, GameModelView, \
    EventJoinView, EventLeaveView, PublisherRoot, PublisherModelView

urlpatterns = patterns('events',
    url(r'^publishers/$', PublisherRoot.as_view(resource=PublisherResource,
        permissions=(IsUserOrIsAnonReadOnly, )), name='publisher-list'),
    url(r'^publishers/(?P<pk>[^/]+)/$', PublisherModelView.as_view(
        resource=PublisherResource, permissions=(IsUserOrIsAnonReadOnly, )),
        name='publisher-instance'),
    
    url(r'^games/$', GameRoot.as_view(resource=GameResource),
        name='game-list'),
    url(r'^games/(?P<pk>[^/]+)/$', GameModelView.as_view(
        resource=GameResource), name='game-instance'),

    url(r'^events/$', EventRoot.as_view(resource=EventResource),
        name='event-list'),
    url(r'^events/(?P<pk>[^/]+)/$', EventModelView.as_view(
        resource=EventResource), name='event-instance'),
    url(r'^events/(?P<pk>[^/]+)/join/$', EventJoinView.as_view(
        resource=EventResource), name='event-instance-join'),
    url(r'^events/(?P<pk>[^/]+)/leave/$', EventLeaveView.as_view(
        resource=EventResource), name='event-instance-leave'),
)