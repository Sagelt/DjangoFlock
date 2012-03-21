from django.conf.urls.defaults import patterns, include, url
from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from events.resources import GameResource, EventResource
from events.views import EventRoot, EventModelView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'DjangoFlock.views.home', name='home'),
    # url(r'^DjangoFlock/', include('DjangoFlock.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^games/$', ListOrCreateModelView.as_view(resource=GameResource)),
    url(r'^games/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=GameResource)),
    url(r'^events/$', EventRoot.as_view()),
    url(r'^events/(?P<pk>[^/]+)/$', EventModelView.as_view(resource=EventResource), name='event-instance'),
)
