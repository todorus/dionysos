from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # url(r'^$', 'django_longitudinal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^longitudinal/', include('django_longitudinal.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
