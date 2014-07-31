from django.test import TestCase
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test.client import Client
import json

from django_longitudinal.views import home
from django_longitudinal.models import DataPoint
from django_longitudinal.views import serializeSingle

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

class RestfullTest(TestCase):

	def setUp(self):
		self.client = Client()

	def test_create_data_point_correct(self):

		oldCount = DataPoint.objects.count()

		# when a JSON request with Method POST is sent to the DataPoint resource, with valid data
		url = reverse("datapoints")
		data = {
			"label": "TempTest",
			"quantity": "Temperature",
			"unit": "celsius"
		}
		response = self.client.post(url, json.dumps(data),content_type="application/json")

		# it creates a new DataPoint entry
		self.assertEqual(DataPoint.objects.count(),oldCount+1)

		# with the correct values
		lastDataPoint = DataPoint.objects.all().reverse()[0]
		self.assertEqual(lastDataPoint.label, data["label"])
		self.assertEqual(lastDataPoint.quantity, data["quantity"])
		self.assertEqual(lastDataPoint.unit, data["unit"])

		# it returns a 201 status
		self.assertEqual(response.status, 201)

		# and returns the created entry as JSON in the body
		data["id"] = lastDataPoint.id
		self.assertEqual(data,lastDataPoint.to_dict())

	def test_create_data_point_incorrect(self):
		
		oldCount = DataPoint.objects.count()

		# when a JSON request with Method POST is sent to the DataPoint resource, with invalid data
		url = reverse("datapoints")
		data = {}
		response = self.client.post(url, json.dumps(data),content_type="application/json")

		# it does not create a new DataPoint entry
		self.assertEqual(DataPoint.objects.count(),oldCount)
		
		# it returns a 400 status
		self.assertEqual(response.status, 400)
		
	"""
	def test_update_data_point(self):
		self.fail("Write test")

		# when a JSON request with Method PUT is sent to the DataPoint resource
		# it finds the entry with the matching id
		# it ignores the unknown properties supplied in the JSON
		# it updates the known properties supplied in the JSON

		
		# it returns a 200 status
		# and returns the updated entry as JSON in the body

	def test_update_data_point_unknown(self):
		self.fail("Write test")

		# when a JSON request with Method PUT is sent to the DataPoint resource
		# with a nonexistant id
		# it updates the properties supplied in the JSON
		
		# it returns a 404 status

	def test_destroy_data_point(self):
		self.fail("Write test")

		# when a request with Method DELETE is sent to the DataPoint resource
		# it deletes the entry with the matching id

		# it returns a 200 status

	def test_destroy_data_point_unknown(self):
		self.fail("Write test")

		# when a request with Method DELETE is sent to the DataPoint resource
		# with a nonexistant id

		# it returns a 404 status

	def test_read_data_point(self):
		self.fail("Write test")

		# when a JSON request with Method GET is sent to the DataPoint resource
		# it finds the entry with the matching id
		
		# it returns a 200 status
		# and returns the found entry as JSON in the body

	def test_read_data_point_unknown(self):
		self.fail("Write test")

		# when a request with Method GET is sent to the DataPoint resource
		# with a nonexistant id

		# it returns a 404 status
	"""