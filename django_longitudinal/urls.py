from django.conf.urls import url
from django_longitudinal import views

urlpatterns = [
  url(r'^$', 'django_longitudinal.views.home', name='home'),
  url(r'^datapoints/(?P<id>[0-9]+)', 'django_longitudinal.views.datapoint',name="datapoint"),
  url(r'^datapoints', 'django_longitudinal.views.datapoints',name="datapoints"),
]