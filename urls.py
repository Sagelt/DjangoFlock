from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from djangorestframework.permissions import IsUserOrIsAnonReadOnly
from djangorestframework.views import InstanceModelView, ListOrCreateModelView
from events.resources import GameResource, EventResource, PublisherResource
from events.views import EventRoot, EventModelView, GameRoot, GameModelView, \
    EventJoinView, EventLeaveView, GameCreate, GameUpdate, GameDelete

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'DjangoFlock.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^publishers/$', ListOrCreateModelView.as_view(resource=PublisherResource, permissions=(IsUserOrIsAnonReadOnly, ))),
    #url(r'^publishers/new/$', GameCreate.as_view()), # Form to create
    url(r'^publishers/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=PublisherResource, permissions=(IsUserOrIsAnonReadOnly, ))),
    #url(r'^publishers/(?P<pk>[^/]+)/edit/$', GameUpdate.as_view()), # Form to edit
    #url(r'^publishers/(?P<pk>[^/]+)/delete/$', GameDelete.as_view()), # Form to delete
    
    url(r'^games/$', GameRoot.as_view(resource=GameResource)),
    url(r'^games/new/$', GameCreate.as_view()), # Form to create
    url(r'^games/(?P<pk>[^/]+)/$', GameModelView.as_view(resource=GameResource)),
    url(r'^games/(?P<pk>[^/]+)/edit/$', GameUpdate.as_view()), # Form to edit
    url(r'^games/(?P<pk>[^/]+)/delete/$', GameDelete.as_view()), # Form to delete

    url(r'^events/$', EventRoot.as_view(resource=EventResource)),
    url(r'^events/(?P<pk>[^/]+)/$', EventModelView.as_view(resource=EventResource), name='event-instance'),
    url(r'^events/(?P<pk>[^/]+)/join/$', EventJoinView.as_view(resource=EventResource)),
    url(r'^events/(?P<pk>[^/]+)/leave/$', EventLeaveView.as_view(resource=EventResource)),
)

urlpatterns += staticfiles_urlpatterns()
