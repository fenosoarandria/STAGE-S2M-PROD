from django.template import loader
from django.http import HttpResponse

def Transformation(request):
    template = loader.get_template('transformationproduit/transformation.html')
    return HttpResponse(template.render())

def Recapitulation(request):
    template = loader.get_template('transformationproduit/recapitulation.html')
    return HttpResponse(template.render())
