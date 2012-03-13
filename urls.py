from django.conf.urls.defaults import patterns, include, url
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from events.models import Game, Event

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

class GameResource(ModelResource):
    model = Game
    
class EventResource(ModelResource):
    model = Event

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
    url(r'^events/$', ListOrCreateModelView.as_view(resource=EventResource)),
    url(r'^events/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=EventResource)),
)
