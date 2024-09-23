from django.http import JsonResponse
from applications.model.releverprix.base_mysql.RelArtNouveau import RelArtNouveau

# ----------------------------------Liste des relevé par article------------------------------------------------------------------------

def liste_rel_art_nouveau(request):
    try:
        # Récupère tous les objets RelArtNouveau
        liste = RelArtNouveau.objects.all().values('gencode', 'libelle', 'libelle_plus', 'prix', 'id_enseigne')
        
        # Convertir les objets en liste de dictionnaires
        data = list(liste)
        
        # Retourner la réponse JSON
        return JsonResponse({'data': data})
    except Exception as e:
        # Retourne une réponse d'erreur JSON en cas d'exception
        return JsonResponse({'error': str(e)}, status=500)
