from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from applications.model.releverprix.base_mysql.Enseigne import Enseigne
from django.views.decorators.csrf import csrf_exempt

from applications.view.releverprix.PersonnelPView import select_by_id_personnel
from applications.view.releverprix.RelLogView import historique


# ----------------------------------Liste des enseigne------------------------------------------------------------------------
def liste_enseigne(request):
    try:
        # Récupère tous les objets RelArtNouveau
        liste = Enseigne.objects.all().values('enseigne_ens', 'libelle_ens', 'lib_plus_ens')
        
        # Convertir les objets en liste de dictionnaires
        data = list(liste)
        # Retourner la réponse JSON
        return JsonResponse({'data': data})
    except Exception as e:
        # Retourne une réponse d'erreur JSON en cas d'exception
        return JsonResponse({'error': str(e)}, status=500)



# ----------------------------------Insertion de l'enseigne------------------------------------------------------------------------
@csrf_exempt
def ajout_enseigne(request):
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom')
            rubrique = request.POST.get('rubrique')
            personnel = select_by_id_personnel(request.session.get('nummatr'))
            

            # Vérification des champs requis
            if not nom:
                return JsonResponse({'success': False, 'message': 'Le nom de l\'enseigne est requis.'})
                
            if not rubrique:
                return JsonResponse({'success': False, 'message': 'La rubrique est requise.'})

            # Création de l'objet Enseigne
            Enseigne.objects.create(
                libelle_ens=nom,
                lib_plus_ens=rubrique,
            )
            data = [
                (request.session.get('nummatr'), "Insertion enseigne", f"{personnel[1]} {personnel[2]} a inséré un nouvel enseigne : - ")
            ]
            historique(data)
            
            return JsonResponse({'success': True, 'message': 'Enseigne ajoutée avec succès !'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur lors de l\'ajout de l\'enseigne : {str(e)}'})
    else:
        return JsonResponse({'success': False, 'message': 'Requête non valide.'})



# ----------------------------------Modification enseigne------------------------------------------------------------------------
@csrf_exempt
def update_enseigne(request, id):
    
    libelle_ens = request.POST.get('nom')
    lib_plus_ens = request.POST.get('rubrique')
    try:
        personnel = select_by_id_personnel(request.session.get('nummatr'))
        
        if request.method == 'POST':
            releve = get_object_or_404(Enseigne, enseigne_ens=id)
            
            # Mettre à jour les champs de l'enregistrement
            releve.lib_plus_ens = lib_plus_ens
            releve.libelle_ens = libelle_ens
            releve.save()
            data = [
                (request.session.get('nummatr'), "Modification enseigne", f" {personnel[1]} {personnel[2]} à modifier l'enseigne numéro: {id}")
            ]
            historique(data)
            
            
            return JsonResponse({'success': True, 'message': 'Enseigne modifié avec succès.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erreur lors de modification de l\'enseigne : {e}'})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})