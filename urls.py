from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from events.resources import GameResource, EventResource
from events.views import EventRoot, EventModelView, GameRoot, GameModelView

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'DjangoFlock.views.home', name='home'),
    # url(r'^DjangoFlock/', include('DjangoFlock.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^games/$', GameRoot.as_view(resource=GameResource)),
    url(r'^games/(?P<pk>[^/]+)/$', GameModelView.as_view(resource=GameResource)),
    url(r'^events/$', EventRoot.as_view()),
    url(r'^events/(?P<pk>[^/]+)/$', EventModelView.as_view(resource=EventResource), name='event-instance'),
)
