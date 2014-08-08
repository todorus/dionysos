from django.test import TestCase
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils import timezone
from django.test.client import Client
import json
from django.core.exceptions import ObjectDoesNotExist

from django_longitudinal.views import home
from django_longitudinal.models import DataPoint
from django_longitudinal.models import Measurement
from django_longitudinal.views import serializeSingle

class DataPointTest(TestCase):

	def setUp(self):
		self.client = Client()

	def test_create_correct(self):

		oldCount = DataPoint.objects.count()

		# when a JSON request with Method POST is sent to the DataPoint resource, with valid data
		url = reverse("datapoints")
		data = {
			"label": "TempTest",
			"quantity": "Temperature",
			"unit": "celsius",
			"datatype":DataPoint.TYPE_FLOAT,
		}
		response = self.client.post(url, json.dumps(data),content_type="application/json")

		# it creates a new DataPoint entry
		self.assertEqual(DataPoint.objects.count(),oldCount+1)

		# with the correct values
		lastDataPoint = DataPoint.objects.all().reverse()[0]
		self.assertEqual(lastDataPoint.label, data["label"])
		self.assertEqual(lastDataPoint.quantity, data["quantity"])
		self.assertEqual(lastDataPoint.unit, data["unit"])
		self.assertEqual(lastDataPoint.datatype, data["datatype"])

		# it returns a 201 status
		self.assertEqual(response.status, 201)

		# and returns the created entry as JSON in the body
		self.assertEqual(json.loads(response.body),lastDataPoint.to_dict())

	def test_create_incorrect(self):
		
		oldCount = DataPoint.objects.count()

		# when a JSON request with Method POST is sent to the DataPoint resource, with invalid data
		url = reverse("datapoints")
		data = {}
		response = self.client.post(url, json.dumps(data),content_type="application/json")

		# it does not create a new DataPoint entry
		self.assertEqual(DataPoint.objects.count(),oldCount)
		
		# it returns a 400 status
		self.assertEqual(response.status, 400)
		
	def test_update(self):
		item = DataPoint()
		item.label = "Inside temperature"
		item.quantity = "temperature"
		item.unit = "°C"
		item.datatype = DataPoint.TYPE_FLOAT
		item.save()

		# when a JSON request with Method PUT is sent to the DataPoint resource
		url = reverse("datapoint", kwargs={"id":item.id})
		data = {
			"label":"Outside wind",
			"quantity": "Velocity",
			"unit": "m/s",
			"datatype": DataPoint.TYPE_FLOAT,
		}
		response = self.client.put(url, json.dumps(data),content_type="application/json")

		# it finds the entry with the matching id
		jsonResponse = json.loads(response.body)
		self.assertEqual(jsonResponse["id"],item.id)
		
		# it updates the known properties supplied in the JSON
		data["id"] = item.id
		testItem = DataPoint.objects.get(pk=item.id)
		self.assertEqual(data, testItem.to_dict())
		
		# it returns a 200 status
		self.assertEqual(response.status, 200)

		# and returns the updated entry as JSON in the body
		self.assertEqual(data, jsonResponse)

	

	def test_update_unknown(self):

		# when a JSON request with Method PUT is sent to the DataPoint resource
		# with a nonexistant id
		url = reverse("datapoint", kwargs={"id":0})
		data = {
			"label":"Outside wind",
			"quantity": "Velocity",
			"unit": "m/s",
			"datatype": DataPoint.TYPE_FLOAT,
		}
		response = self.client.put(url, json.dumps(data),content_type="application/json")
		
		# it returns a 404 status
		self.assertEqual(response.status, 404)

	
	
	def test_destroy(self):
		item = DataPoint()
		item.label = "Inside temperature"
		item.quantity = "temperature"
		item.unit = "°C"
		item.datatype = DataPoint.TYPE_FLOAT
		item.save()

		oldCount = DataPoint.objects.count()

		# when a request with Method DELETE is sent to the DataPoint resource
		url = reverse("datapoint", kwargs={"id":item.id})
		response = self.client.delete(url)

		# it deletes the entry with the matching id
		self.assertEqual(oldCount-1,DataPoint.objects.count())
		self.assertRaises(ObjectDoesNotExist, lambda: DataPoint.objects.get(pk=item.id))

		# it returns a 200 status
		self.assertEqual(response.status, 200)

	def test_destroy_unknown(self):

		# when a request with Method DELETE is sent to the DataPoint resource
		# with a nonexistant id
		url = reverse("datapoint", kwargs={"id":0})
		response = self.client.delete(url)

		# it returns a 404 status
		self.assertEqual(response.status, 404)


	def test_read(self):

		item = DataPoint()
		item.label = "Inside temperature"
		item.quantity = "temperature"
		item.unit = "°C"
		item.datatype = DataPoint.TYPE_FLOAT
		item.save()

		# when a JSON request with Method GET is sent to the DataPoint resource
		# it finds the entry with the matching id
		url = reverse("datapoint", kwargs={"id":item.id})
		response = self.client.get(url,content_type="application/json")
		
		# it returns a 200 status
		self.assertEqual(response.status, 200)

		# and returns the found entry as JSON in the body
		self.assertEqual(json.loads(response.body),item.to_dict())


	def test_read_unknown(self):

		# when a request with Method GET is sent to the DataPoint resource
		# with a nonexistant id
		url = reverse("datapoint", kwargs={"id":0})
		response = self.client.get(url,content_type="application/json")

		# it returns a 404 status
		self.assertEqual(response.status, 404)


class MeasurementTest(TestCase):

	def setUp(self):
		self.client = Client()

	def test_create_correct(self):

		datapoint = DataPoint()
		datapoint.label = "Inside temperature"
		datapoint.quantity = "temperature"
		datapoint.unit = "°C"
		datapoint.datatype = DataPoint.TYPE_FLOAT
		datapoint.save()

		oldCount = Measurement.objects.count()

		# when a JSON request with Method POST is sent to a Measurements endpoint, with valid data
		url = reverse("measurements", kwargs={"datapoint_id":datapoint.id})
		data = {
			"value": 1.0,
			"time": timezone.now().isoformat(),
		}
		response = self.client.post(url, json.dumps(data),content_type="application/json")

		# it creates a new Measurement entry
		self.assertEqual(Measurement.objects.count(),oldCount+1)

		# with the correct values
		lastMeasurement = Measurement.objects.all().reverse()[0]
		self.assertEqual(lastMeasurement.valueFloat, data["value"])
		self.assertEqual(lastMeasurement.time.isoformat(), data["time"])

		# it returns a 201 status
		self.assertEqual(response.status, 201)

		# and returns the created entry as JSON in the body
		self.assertEqual(json.loads(response.body),lastMeasurement.to_dict())

	def test_create_correct_notime(self):

		datapoint = DataPoint()
		datapoint.label = "Inside temperature"
		datapoint.quantity = "temperature"
		datapoint.unit = "°C"
		datapoint.datatype = DataPoint.TYPE_FLOAT
		datapoint.save()

		oldCount = Measurement.objects.count()

		# when a JSON request with Method POST is sent to a Measurements endpoint, with valid data
		url = reverse("measurements", kwargs={"datapoint_id":datapoint.id})
		data = {
			"value": 1.0,
		}
		response = self.client.post(url, json.dumps(data),content_type="application/json")

		# it creates a new Measurement entry
		self.assertEqual(Measurement.objects.count(),oldCount+1)

		# with the correct values
		lastMeasurement = Measurement.objects.all().reverse()[0]
		self.assertEqual(lastMeasurement.valueFloat, data["value"])

		# it returns a 201 status
		self.assertEqual(response.status, 201)

	def test_create_incorrect(self):

		datapoint = DataPoint()
		datapoint.label = "Inside temperature"
		datapoint.quantity = "temperature"
		datapoint.unit = "°C"
		datapoint.datatype = DataPoint.TYPE_FLOAT
		datapoint.save()

		oldCount = Measurement.objects.count()

		# when a JSON request with Method POST is sent to a Measurements endpoint, with valid data
		url = reverse("measurements", kwargs={"datapoint_id":datapoint.id})
		data = {
		}
		response = self.client.post(url, json.dumps(data),content_type="application/json")

		# it DOES NOT create a new Measurement entry
		self.assertEqual(Measurement.objects.count(),oldCount)

		# it returns a 400 status
		self.assertEqual(response.status, 400)

	def test_update(self):
		datapoint = DataPoint()
		datapoint.label = "Inside temperature"
		datapoint.quantity = "temperature"
		datapoint.unit = "°C"
		datapoint.datatype = DataPoint.TYPE_FLOAT
		datapoint.save()

		oldTime = timezone.now()
		measurement = Measurement()
		measurement.datapoint = datapoint
		measurement.valueFloat = 20
		measurement.time = oldTime
		measurement.save()

		# when a JSON request with Method PUT is sent to the Measurement resource
		url = reverse("measurement", kwargs={"datapoint_id":datapoint.id, "measurement_id":measurement.id})
		data = {
			"value":10,
			"time": timezone.now().isoformat(),
		}
		response = self.client.put(url, json.dumps(data),content_type="application/json")

		# it finds the entry with the matching id
		jsonResponse = json.loads(response.body)
		self.assertEqual(jsonResponse["id"],measurement.id)
		
		# it updates the known properties supplied in the JSON
		data["id"] = measurement.id
		testItem = Measurement.objects.get(pk=measurement.id)
		self.assertEqual(data, testItem.to_dict())
		
		# it returns a 200 status
		self.assertEqual(response.status, 200)

		# and returns the updated entry as JSON in the body
		self.assertEqual(data, jsonResponse)

	def test_update_unknown(self):
		# when a JSON request with Method PUT is sent to the Measurement resource
		# with a nonexistant id
		datapoint = DataPoint()
		datapoint.label = "Inside temperature"
		datapoint.quantity = "temperature"
		datapoint.unit = "°C"
		datapoint.datatype = DataPoint.TYPE_FLOAT
		datapoint.save()

		# when a JSON request with Method PUT is sent to the Measurement resource
		url = reverse("measurement", kwargs={"datapoint_id":datapoint.id, "measurement_id":0})
		data = {
			"value":10,
			"time": timezone.now().isoformat(),
		}
		response = self.client.put(url, json.dumps(data),content_type="application/json")
		
		# it returns a 404 status
		self.assertEqual(response.status, 404)

	def test_destroy(self):
		datapoint = DataPoint()
		datapoint.label = "Inside temperature"
		datapoint.quantity = "temperature"
		datapoint.unit = "°C"
		datapoint.datatype = DataPoint.TYPE_FLOAT
		datapoint.save()

		oldTime = timezone.now()
		measurement = Measurement()
		measurement.datapoint = datapoint
		measurement.valueFloat = 20
		measurement.time = oldTime
		measurement.save()

		oldCount = Measurement.objects.count()

		# when a JSON request with Method DELETE is sent to the Measurement resource
		url = reverse("measurement", kwargs={"datapoint_id":datapoint.id, "measurement_id":measurement.id})
		response = self.client.delete(url)

		# it deletes the entry with the matching id
		self.assertEqual(oldCount-1,Measurement.objects.count())
		self.assertRaises(ObjectDoesNotExist, lambda: Measurement.objects.get(pk=measurement.id))

		# it returns a 200 status
		self.assertEqual(response.status, 200)

	def test_destroy_unknown(self):
		datapoint = DataPoint()
		datapoint.label = "Inside temperature"
		datapoint.quantity = "temperature"
		datapoint.unit = "°C"
		datapoint.datatype = DataPoint.TYPE_FLOAT
		datapoint.save()

		# when a request with Method DELETE is sent to the Measurement resource
		# with a nonexistant id
		url = reverse("measurement", kwargs={"datapoint_id":datapoint.id, "measurement_id":0})
		response = self.client.delete(url)

		# it returns a 404 status
		self.assertEqual(response.status, 404)

"""
	def test_read(self):
		self.fail("Write test")


	def test_read_unknown(self):
		self.fail("Write test")
"""	