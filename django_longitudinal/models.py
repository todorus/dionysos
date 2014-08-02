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
