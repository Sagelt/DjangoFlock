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
    url(r'^games/$', 'events.views.list_games'),
    url(r'^games/new/$', 'events.views.create_game_form'),
    url(r'^games/(?P<id>\d+)/$', 'events.views.retrieve_game'),
    url(r'^games/(?P<id>\d+)/edit/$', 'events.views.edit_game_form'),
    url(r'^games/(?P<id>\d+)/delete/$', 'events.views.delete_game_form'),
)
