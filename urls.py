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
    
    # User profile interface
    url(r'users/$', views.users_list),
    url(r'users/(?P<username>[^/]+)/$', views.users_instance),

    # HTML forms for accessing the REST API.
    url('^publishers/$', views.publishers_list),
    url('^publishers/new/$', views.publishers_new),
    url('^publishers/(?P<pk>[^/]+)/$', views.publishers_instance),
    url('^publishers/(?P<pk>[^/]+)/edit/$', views.publishers_instance_edit),

    url('^games/$', views.games_list),
    url('^games/new/$', views.games_new),
    url('^games/(?P<pk>[^/]+)/$', views.games_instance),
    url('^games/(?P<pk>[^/]+)/edit/$', views.games_instance_edit),

    url('^conventions/$', views.conventions_list),
    url('^conventions/new/$', views.conventions_new),
    url('^conventions/(?P<pk>[^/]+)/$', views.conventions_instance),
    url('^conventions/(?P<pk>[^/]+)/edit/$', views.conventions_instance_edit),

    url('^events/$', views.events_list),
    url('^events/new/$', views.events_new),
    url('^events/(?P<pk>[^/]+)/$', views.events_instance),
    url('^events/(?P<pk>[^/]+)/edit/$', views.events_instance_edit),
    url('^events/(?P<pk>[^/]+)/join/$', views.events_instance_join),
    url('^events/(?P<pk>[^/]+)/leave/$', views.events_instance_leave),

    url('^demands/$', views.demands_list),
    url('^demands/mine/$', views.demands_list_mine),
    url('^demands/new/$', views.demands_new),
    url('^demands/(?P<pk>[^/]+)/$', views.demands_instance),
    url('^demands/(?P<pk>[^/]+)/edit/$', views.demands_instance_edit),
)

urlpatterns += staticfiles_urlpatterns()
