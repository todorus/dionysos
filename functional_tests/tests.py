from django_longitudinal.models import DataPoint
from django_longitudinal.models import Measurement
from django_longitudinal.models import Observable
from selenium import webdriver
from django.test import LiveServerTestCase

class DisplayTest(LiveServerTestCase):

  def setUp(self):
    self.browser = webdriver.Chrome()
    self.browser.implicitly_wait(3)

    observable1 = Observable()
    observable1.label = "InsideObservable"
    observable1.save()
    observable2 = Observable()
    observable2.label = "OutsideObservable"
    observable2.save()

    datapoint1 = DataPoint()
    datapoint1.label = "Inside temperature"
    datapoint1.quantity = "temperature"
    datapoint1.unit = "°C"
    datapoint1.datatype = DataPoint.TYPE_FLOAT
    datapoint1.observable_id = observable1.id
    datapoint1.save()
    datapoint2 = DataPoint()
    datapoint2.label = "Inside wind"
    datapoint2.quantity = "velocity"
    datapoint2.unit = "m/s"
    datapoint2.datatype = DataPoint.TYPE_FLOAT
    datapoint2.observable_id = observable1.id
    datapoint2.save()

    datapoint3 = DataPoint()
    datapoint3.label = "Outside temperature"
    datapoint3.quantity = "temperature"
    datapoint3.unit = "°C"
    datapoint3.datatype = DataPoint.TYPE_FLOAT
    datapoint3.observable_id = observable2.id
    datapoint3.save()
    datapoint4 = DataPoint()
    datapoint4.label = "Outside wind"
    datapoint4.quantity = "velocity"
    datapoint4.unit = "m/s"
    datapoint4.datatype = DataPoint.TYPE_FLOAT
    datapoint4.observable_id = observable2.id
    datapoint4.save()

  def tearDown(self):
    self.browser.quit()

  def test_shows_observables(self):
    self.browser.get(self.live_server_url)
