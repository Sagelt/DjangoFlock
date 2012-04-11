from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import views

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # REST API
    url(r'^api/', include('events.urls')),
    #url(r'^api1/', include('events.urls')),

    # HTML forms for accessing the REST API.
    url('^publishers/$', views.publishers_list),
    url('^publishers/(?P<pk>[^/]+)/$', views.publishers_instance),
    url('^games/$', views.games_list),
    url('^games/(?P<pk>[^/]+)/$', views.games_instance),
    url('^events/$', views.events_list),
    url('^events/(?P<pk>[^/]+)/$', views.events_instance),
)

urlpatterns += staticfiles_urlpatterns()
