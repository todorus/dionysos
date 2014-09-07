from django.conf.urls import url
from django_longitudinal import views

urlpatterns = [
  url(r'^$', 'django_longitudinal.views.home', name='home'),
  url(r'^datapoints/(?P<datapoint_id>[0-9]+)/measurements/(?P<measurement_id>[0-9]+)', 'django_longitudinal.views.measurement',name="measurement"),
  url(r'^datapoints/(?P<datapoint_id>[0-9]+)/measurements', 'django_longitudinal.views.measurements',name="measurements"),
  url(r'^datapoints/(?P<datapoint_id>[0-9]+)/assign/(?P<observable_id>[0-9]+)', 'django_longitudinal.views.assignObservable',name="assign_observable"),
  url(r'^datapoints/(?P<id>[0-9]+)', 'django_longitudinal.views.datapoint',name="datapoint"),
  url(r'^datapoints', 'django_longitudinal.views.datapoints',name="datapoints"),
  url(r'^observables/(?P<id>[0-9]+)', 'django_longitudinal.views.observable',name="observable"),
  url(r'^observables', 'django_longitudinal.views.observables',name="observables"),
]