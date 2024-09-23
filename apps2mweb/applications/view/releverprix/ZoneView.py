from django.db import connections
from django.shortcuts import get_object_or_404
from applications.model.releverprix.base_mysql.Zone import Zone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from applications.view.releverprix.PersonnelPView import select_by_id_personnel
from applications.view.releverprix.RelLogView import historique

# ----------------------------------Selection de liste des zones------------------------------------------------------------------------
def liste_zone(request):
    try:
        # Récupère tous les objets RelArtNouveau
        liste = Zone.objects.all().values('zone_zn', 'libelle_zn', 'lib_plus_zn')
        # Convertir les objets en liste de dictionnaires
        data = list(liste)
        # Retourner la réponse JSON
        return JsonResponse({'data': data})
    except Exception as e:
        # Retourne une réponse d'erreur JSON en cas d'exception
        return JsonResponse({'error': str(e)}, status=500)


# ---------------------------------- Insertion nouveau zone ------------------------------------------------------------------------
@csrf_exempt
def ajout_zone(request):
    if request.method == 'POST':
        try:
            personnel = select_by_id_personnel(request.session.get('nummatr'))
            # Récupérer les données du formulaire
            ville = request.POST.get('ville')
            zone = request.POST.get('zone')

            # Vérifier les champs requis
            if not ville:
                return JsonResponse({'success': False, 'message': 'Le nom de la zone est requis.'})
                
            if not zone:
                return JsonResponse({'success': False, 'message': 'La rubrique est requise.'})

            # Création de l'objet Zone
            Zone.objects.create(
                libelle_zn=ville,
                lib_plus_zn=zone,
            )
            
            data = [
                (request.session.get('nummatr'), "Creation zone  ", f"{personnel[1]} {personnel[2]} a ajouter des nouveaux zone")
            ]
            historique(data)
            
            return JsonResponse({'success': True, 'message': 'Zone ajoutée avec succès !'})

        except Exception as e:
            # Capturer et afficher l'erreur
            return JsonResponse({'success': False, 'message': f'Erreur lors de l\'ajout de la zone : {str(e)}'})
    else:
        return JsonResponse({'success': False, 'message': 'Requête non valide.'})# ----------------------------------Modification zone------------------------------------------------------------------------


# ---------------------------------- Modification nouveau zone ------------------------------------------------------------------------
@csrf_exempt
def update_zone(request, id):
    
    libelle_zn = request.POST.get('ville')
    lib_plus_zn = request.POST.get('zone')
    try:
        personnel = select_by_id_personnel(request.session.get('nummatr'))
        if request.method == 'POST':
            releve = get_object_or_404(Zone, zone_zn=id)
            
            # Mettre à jour les champs de l'enregistrement
            releve.lib_plus_zn = lib_plus_zn
            releve.libelle_zn = libelle_zn
            releve.save()
            data = [
                (request.session.get('nummatr'), "Modification  ", f"{personnel[1]} {personnel[2]} a modifier la zone numero:{id}")
            ]
            historique(data)
            return JsonResponse({'success': True, 'message': 'Zone modifié avec succès.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erreur lors de modification de zone : {e}'})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})


# ---------------------------------- Select by id zone ------------------------------------------------------------------------
def select_by_id_zone(request,zone_zn):
        # Requête SQL pour sélectionner le libelle par ID
        query = "SELECT libelle_zn FROM rel_zone_prix WHERE zone_zn = %s"
        params = [zone_zn]
    
        # Exécuter la requête SQL
        with connections['default'].cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchone()
        return rows