from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from django_longitudinal.views import home
from django_longitudinal.models import DataPoint

# Create your tests here.

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve("/")
		self.assertEqual(found.func, home)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home(request)

		self.assertTrue(response.content.startswith(b"<html>"))
		self.assertIn(b"<title>Variables</title>",response.content)
		self.assertTrue(response.content.endswith(b"</html>"))

class DataPointTest(TestCase):

	def test_saving_and_retrieving_datapoints(self):
		item1 = DataPoint()
		item1.label = "Inside temperature"
		item1.quantity = "temperature"
		item1.unit = "°C"
		item1.save()

		item2 = DataPoint()
		item2.label = "Outside light"
		item2.quantity = "Luminance"
		item2.unit = "cd/m^2"
		item2.save()

		saved_items = DataPoint.objects.all()
		self.assertEqual(saved_items.count(),2)

		saved1 = saved_items[0]
		saved2 = saved_items[1]

		self.assertEqual(saved1.label, item1.label)
		self.assertEqual(saved1.quantity, item1.quantity)
		self.assertEqual(saved1.unit, item1.unit)

		self.assertEqual(saved2.label, item2.label)
		self.assertEqual(saved2.quantity, item2.quantity)
		self.assertEqual(saved2.unit, item2.unit)
