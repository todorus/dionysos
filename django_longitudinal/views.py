from django.shortcuts import render
from django.http import HttpResponse
from django_longitudinal.models import DataPoint
import json
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

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

	return response

def datapoint(request, id):
	response = HttpResponse()
	response.status = 400
	# entry = DataPoint.objects.get(pk=id)
	# try:
	# 	pass
	# except Exception, e:
	# 	raise e

	try:
		if request.method == GET:
			response.body = "get"
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

def getBody(request):
	if isinstance(request.body, bytes):
		return request.body.decode('utf-8')
	return request.body

def serializeSingle(entry):
	data = serializers.serialize('json', [entry,])
	struct = json.loads(data)
	data = json.dumps(struct[0])
	return data