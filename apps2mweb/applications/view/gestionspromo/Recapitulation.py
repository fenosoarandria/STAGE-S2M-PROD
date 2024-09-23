from django.http import HttpResponse
from django.template import loader
import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)

def AffichageRecapitulation(request):
    context = {
        'apply_custom_styles': True,
    }
    return render(request, 'recapproduction/entree_produit_fini.html', context)


def AffichageRegularisation(request):
    context = {
        'apply_regularisation_produit': True,
    }
    return render(request, 'recapproduction/regularisation_produit.html', context)