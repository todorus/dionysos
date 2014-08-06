from django.shortcuts import render
from django.http import HttpResponse
from django_longitudinal.models import DataPoint
from django_longitudinal.models import Measurement
from django.utils import timezone
import json
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

import pdb

# Create your views here.
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

def home(request):
	return HttpResponse("<html><head><title>Variables</title></head><body></body></html>")

def datapoints(request):
	response = HttpResponse()
	response.status = 400

	if request.method == GET:
		debug = 1
	elif request.method == POST:
		data = json.loads(getBody(request))

		try:
			entry = DataPoint(**data)
			entry.full_clean()
			entry.save()

			response.body = entry.to_json()
			response.status = 201
		except ValidationError:
			response.status = 400
		except IntegrityError:
			response.status = 400

	return response

def datapoint(request, id):
	response = HttpResponse()
	response.status = 400

	try:
		if request.method == GET:
			response.body = DataPoint.objects.get(pk=id).to_json()
			response.status = 200
		elif request.method == PUT:
			data = json.loads(getBody(request))
			DataPoint.objects.filter(pk=id).update(**data)
			response.body = DataPoint.objects.get(pk=id).to_json()
			response.status = 200
		elif request.method == DELETE:
			DataPoint.objects.get(pk=id).delete()
			response.status = 200
	except ObjectDoesNotExist:
			response.status = 404

	return response

def measurements(request, datapoint_id):
	response = HttpResponse()
	response.status = 400

	if request.method == GET:
		debug = 1
	elif request.method == POST:
		data = json.loads(getBody(request))

	try:
		datapoint = DataPoint.objects.get(pk=datapoint_id)
		entry = Measurement()
		entry.datapoint = datapoint

		if(datapoint.datatype == DataPoint.TYPE_STRING):
			entry.valueString = data["value"]
		elif(datapoint.datatype == DataPoint.TYPE_INTEGER):
			entry.valueInt = data["value"]
		elif(datapoint.datatype == DataPoint.TYPE_FLOAT):
			entry.valueFloat = data["value"]
		elif(datapoint.datatype == DataPoint.TYPE_IMAGE):
			debug = 1

		if("time" in data):
			time = data["time"]
		else:
			time = timezone.now()
		entry.time = time

		entry.full_clean()
		entry.save()

		response.body = entry.to_json()
		response.status = 201
	except ValidationError:
		response.status = 400
	except IntegrityError:
		response.status = 400
	except KeyError:
		response.status = 400

	return response


def measurement(request, datapoint_id, measurement_id):
	return None

def getBody(request):
	if isinstance(request.body, bytes):
		return request.body.decode('utf-8')
	return request.body

def serializeSingle(entry):
	data = serializers.serialize('json', [entry,])
	struct = json.loads(data)
	data = json.dumps(struct[0])
	return data