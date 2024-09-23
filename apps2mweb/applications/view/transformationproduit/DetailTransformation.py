from django.template import loader
from django.http import HttpResponse


def TransformationValeur(request):
    template = loader.get_template('transformationproduit/transformationvaleur.html')
    return HttpResponse(template.render())