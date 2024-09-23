from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseNotFound


def PageError(request,exception=None):
    return render(request, 'errorpage/pageerreur.html', status=404)
    
def custom_server_error(request):
    return render(request, 'errorpage/500.html', {}, status=500)