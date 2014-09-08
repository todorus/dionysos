from django.shortcuts import render

def home(request):
  return HttpResponse("<html><head><title>Variables</title></head><body></body></html>")
