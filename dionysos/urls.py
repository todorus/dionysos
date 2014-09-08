from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^longitudinal/', include('django_longitudinal.urls')),
    url(r'^$', 'webadmin.views.home', name='home'),
)
