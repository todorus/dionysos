from django.db import models
import json

# Create your models here.

class DataPoint(models.Model):
	label = models.CharField(max_length=200)
	quantity = models.CharField(max_length=200)
	unit = models.CharField(max_length=50)

	def to_dict(self):
		return {
			"id":self.id,
			"label":self.label,
			"quantity":self.quantity,
			"unit":self.unit
		}

	def to_json(self):
		return json.dumps(self.to_dict())
