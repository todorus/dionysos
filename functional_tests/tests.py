from django_longitudinal.models import DataPoint
from django_longitudinal.models import Measurement
from django_longitudinal.models import Observable
from selenium import webdriver
from django.test import LiveServerTestCase

class DisplayTest(LiveServerTestCase):

  def setUp(self):
    self.browser = webdriver.Chrome()
    self.browser.implicitly_wait(3)

    self.observable1 = Observable()
    self.observable1.label = "InsideObservable"
    self.observable1.save()
    self.observable2 = Observable()
    self.observable2.label = "OutsideObservable"
    self.observable2.save()

    self.datapoint1 = DataPoint()
    self.datapoint1.label = "Inside temperature"
    self.datapoint1.quantity = "temperature"
    self.datapoint1.unit = "°C"
    self.datapoint1.datatype = DataPoint.TYPE_FLOAT
    self.datapoint1.observable_id = self.observable1.id
    self.datapoint1.save()
    self.datapoint2 = DataPoint()
    self.datapoint2.label = "Inside wind"
    self.datapoint2.quantity = "velocity"
    self.datapoint2.unit = "m/s"
    self.datapoint2.datatype = DataPoint.TYPE_FLOAT
    self.datapoint2.observable_id = self.observable1.id
    self.datapoint2.save()

    self.datapoint3 = DataPoint()
    self.datapoint3.label = "Outside temperature"
    self.datapoint3.quantity = "temperature"
    self.datapoint3.unit = "°C"
    self.datapoint3.datatype = DataPoint.TYPE_FLOAT
    self.datapoint3.observable_id = self.observable2.id
    self.datapoint3.save()
    self.datapoint4 = DataPoint()
    self.datapoint4.label = "Outside wind"
    self.datapoint4.quantity = "velocity"
    self.datapoint4.unit = "m/s"
    self.datapoint4.datatype = DataPoint.TYPE_FLOAT
    self.datapoint4.observable_id = self.observable2.id
    self.datapoint4.save()

  def tearDown(self):
    self.browser.quit()

  def test_shows_observables(self):
    self.browser.get(self.live_server_url)

    # it can find two observables
    self.assertEquals(len(self.browser.find_elements_by_css_selector(".observable")),2)
    # with the correct titles
    titles = self.browser.find_elements_by_css_selector(".observable h3")
    self.assertEquals(len(titles),2)
    assertEquals(titles[0],self.observable1.label)
    assertEquals(titles[1],self.observable2.label)
