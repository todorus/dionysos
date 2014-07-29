from django.shortcuts import render
from django.http import HttpResponse
from django_longitudinal.models import DataPoint
import json
from django.core import serializers

# Create your views here.
GET = 'GET'
POST = 'POST'
UPDATE = 'UPDATE'
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

		entry = DataPoint(**data)
		entry.save()

		response.body = entry.to_json()
		response.status = 201
	else:
		response.status = 400

	return response

def datapoint(request, id):
	if request.method == GET:
		return None
	elif request.method == UPDATE:
		return None
	elif request.method == DELETE:
		return None
	else:
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