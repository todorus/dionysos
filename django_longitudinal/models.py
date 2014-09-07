from django.db import models
import json
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class Observable(models.Model):
	label = models.CharField(max_length=200)

	def to_dict(self):
		return {
			"id": self.id,
			"label":self.label,
		}

	def to_json(self):
		return json.dumps(self.to_dict())

class DataPoint(models.Model):
	TYPE_STRING = 1
	TYPE_INTEGER = 2
	TYPE_FLOAT = 3
	TYPE_IMAGE = 4
	TYPE_CHOICES = (
		(TYPE_STRING, "String"),
		(TYPE_INTEGER, "Integer"),
		(TYPE_FLOAT, "Float"),
		(TYPE_IMAGE, "Image"),
	)

	label = models.CharField(max_length=200)
	quantity = models.CharField(max_length=200)
	unit = models.CharField(max_length=50)
	datatype = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
	observable = models.ForeignKey(Observable, null=True, blank=True)

	def to_dict(self):
		return {
			"id":self.id,
			"label":self.label,
			"quantity":self.quantity,
			"unit":self.unit,
			"datatype":self.datatype,
		}

	def to_json(self):
		return json.dumps(self.to_dict())

class Measurement(models.Model):
	datapoint = models.ForeignKey(DataPoint)
	valueInt = models.IntegerField(null=True, blank=True)
	valueFloat = models.FloatField(null=True, blank=True)
	valueString = models.CharField(max_length=200,null=True, blank=True)
	time = models.DateTimeField()

	def setData(self,value=None,time=None):
		if(self.datapoint.datatype == DataPoint.TYPE_STRING):
			self.valueString = value
		elif(self.datapoint.datatype == DataPoint.TYPE_INTEGER):
			self.valueInt = value
		elif(self.datapoint.datatype == DataPoint.TYPE_FLOAT):
			self.valueFloat = value
		elif(self.datapoint.datatype == DataPoint.TYPE_IMAGE):
			debug = 1

		if(time != None):
			self.time = time
		else:
			self.time = timezone.now()

	def to_dict(self):
		if(self.datapoint.datatype == DataPoint.TYPE_STRING):
			value = self.valueString
		elif(self.datapoint.datatype == DataPoint.TYPE_INTEGER):
			value = self.valueInt
		elif(self.datapoint.datatype == DataPoint.TYPE_FLOAT):
			value = self.valueFloat
		elif(datapoint.datatype == DataPoint.TYPE_IMAGE):
			debug = 1

		return {
			"id": self.id,
			"value":value,
			"time": self.time.isoformat()
		}

	def to_json(self):
		return json.dumps(self.to_dict())

	def clean(self):
		super(Measurement, self).clean()

		if((self.datapoint.datatype == DataPoint.TYPE_STRING and self.valueString == None) or (self.datapoint.datatype == DataPoint.TYPE_INTEGER and self.valueInt == None) or (self.datapoint.datatype == DataPoint.TYPE_FLOAT and self.valueFloat == None)):
			raise ValidationError('Measurement must have a value')

