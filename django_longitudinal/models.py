from django.db import models

# Create your models here.

class DataPoint(models.Model):
	label = models.CharField(max_length=200)
	quantity = models.CharField(max_length=200)
	unit = models.CharField(max_length=50)
