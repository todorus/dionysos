from django.conf.urls import url
from django_longitudinal import views

urlpatterns = [
  url(r'^$', 'django_longitudinal.views.home', name='home'),
]