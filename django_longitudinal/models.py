from django.db import models
import json

# Create your models here.

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
			"value":value,
			"time":str(self.time)
		}

	def to_json(self):
		return json.dumps(self.to_dict())

