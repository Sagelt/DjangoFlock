from django.conf.urls import patterns, include, url
from djangorestframework.permissions import IsUserOrIsAnonReadOnly
from djangorestframework.views import InstanceModelView, ListOrCreateModelView, \
    ListModelView
from events.resources import ConventionResource, GameResource, PublisherResource, \
    DemandResource, UserResource
from events.views import ApiRoot, EventRoot, EventModelView, EventJoinView, \
    EventLeaveView, DemandRoot, DemandModelView, UserModelView

urlpatterns = patterns('events',
    url(r'^$', ApiRoot.as_view()),

    url(r'^publishers/$', ListOrCreateModelView.as_view(
        resource=PublisherResource, permissions=(IsUserOrIsAnonReadOnly, )),
        name='publisher-list'),
    url(r'^publishers/(?P<pk>[^/]+)/$', InstanceModelView.as_view(
        resource=PublisherResource, permissions=(IsUserOrIsAnonReadOnly, )),
        name='publisher-instance'),
    
    url(r'^games/$', ListOrCreateModelView.as_view(resource=GameResource,
        permissions=(IsUserOrIsAnonReadOnly, )), name='game-list'),
    url(r'^games/(?P<pk>[^/]+)/$', InstanceModelView.as_view(
        resource=GameResource, permissions=(IsUserOrIsAnonReadOnly, )),
        name='game-instance'),

    url(r'^conventions/$', ListOrCreateModelView.as_view(
        resource=ConventionResource, permissions=(IsUserOrIsAnonReadOnly, )),
        name='convention-list'),
    url(r'^conventions/(?P<pk>[^/]+)$', InstanceModelView.as_view(
        resource=ConventionResource, permissions=(IsUserOrIsAnonReadOnly, )),
        name='convention-instance'),

    url(r'^events/$', EventRoot.as_view(), name='event-list'),
    url(r'^events/(?P<pk>[^/]+)/$', EventModelView.as_view(),
        name='event-instance'),
    url(r'^events/(?P<pk>[^/]+)/join/$', EventJoinView.as_view(),
        name='event-instance-join'),
    url(r'^events/(?P<pk>[^/]+)/leave/$', EventLeaveView.as_view(),
        name='event-instance-leave'),

    url(r'^demands/$', DemandRoot.as_view(), name='demand-list'),
    url(r'^demands/(?P<pk>[^/]+)$', DemandModelView.as_view(),
        name='demand-instance'),
                       
    url(r'users/$', ListModelView.as_view(resource=UserResource),
        name='user-list'),
    url(r'users/(?P<username>[^/]+)/$', UserModelView.as_view())
)