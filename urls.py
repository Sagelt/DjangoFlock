from django.conf.urls.defaults import patterns, include, url

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
    
    # Events and Games
    url(r'^/games/$', include('events.views.list_games')),
    url(r'^/games/new/$', include('events.views.create_game')),
    url(r'^/games/(?P<id>\d+)/$', include('events.views.retrieve_game')),
    url(r'^/games/(?P<id>\d+)/edit/$', include('events.views.edit_game_form')),
    url(r'^/games/(?P<id>\d+)/delete/$', include('events.views.delete_game_form')),
)
