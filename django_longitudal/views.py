from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
	return HttpResponse("<html><head><title>Variables</title></head><body></body></html>")