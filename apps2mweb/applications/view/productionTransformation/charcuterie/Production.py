from django.http import HttpResponse
from django.template import loader


def CharcAffichage(request):
    template = loader.get_template('productionTransformation/charcuterie/production.html')
    return HttpResponse(template.render())