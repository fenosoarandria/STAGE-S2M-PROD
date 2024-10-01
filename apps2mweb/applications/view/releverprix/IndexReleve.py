from django.db import transaction
from django.http import JsonResponse
from django.db import connections
from django.shortcuts import render, get_object_or_404
from applications.model.releverprix.base_mysql.Enseigne import Enseigne
from applications.model.releverprix.base_mysql.IndexReleve import IndexReleve
from applications.model.releverprix.base_mysql.RelReleve import RelReleve
from applications.model.releverprix.base_mysql.Zone import Zone
from datetime import datetime
from django.db import connection, transaction
from django.views.decorators.csrf import csrf_exempt
from applications.model.releverprix.base_postgres.sifaka_postgres.Fournisseur import Fournisseur
from applications.model.releverprix.base_postgres.sifaka_postgres.Rayon import Rayon
from applications.view.releverprix.PersonnelPView import select_by_id_personnel
from applications.view.releverprix.RelLogView import historique


# ----------------------------------Accueil------------------------------------------------------------------------
def index(request):
    """Affiche tous les relevés avec les données nécessaires pour le template."""
    # Récupérer toutes les instances nécessaires
    context = {
        'enseigne': Enseigne.objects.all(),
        'zone': Zone.objects.all(),
        'rel_releve': RelReleve.objects.values('ref_rel', 'libelle_art_rel'),
        'rayon': Rayon.objects.using('sifaka-postgres').values('rayon', 'rayl30c'),
        'fournisseur': Fournisseur.objects.using('sifaka-postgres').values('id_frs', 'raison_social_frs'),
    }
    return render(request, 'releverprix/index.html', context)
# ----------------------------------Listes relevé------------------------------------------------------------------------

def liste_releve(request):
    sql_query = '''
    SELECT 
        r.*, e.libelle_ens, e.lib_plus_ens, z.libelle_zn, z.lib_plus_zn, et.lib_etat_rel
        FROM rel_index_releve r
        JOIN rel_enseigne e ON r.enseigne_releve = e.enseigne_ens
        JOIN rel_zone_prix z ON r.zone_releve = z.zone_zn
        JOIN rel_etat et ON r.etat_rel = et.rel_etat_code 
        ORDER BY r.id_releve ASC
    '''
    # Exécuter la requête SQL
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        description = cursor.description

    # Vérifie si la requête retourne des résultats
    if description is None:
        return JsonResponse({'data': [], 'error': 'No results found'}, safe=False)

    # Construire le résultat au format JSON
    columns = [col[0] for col in description]
    results = [dict(zip(columns, row)) for row in rows]
    return JsonResponse({'data': results}, safe=False)


# ----------------------------------Filtre liste relevé------------------------------------------------------------------------
@csrf_exempt
def applique_filtre_releve(request):
    """Applique les filtres sur les relevés et retourne les résultats au format JSON."""
    date_debut = request.POST.get('date-debut')
    date_fin = request.POST.get('date-fin')
    concurrent = request.POST.get('concurrent')
    
    # Si aucune date n'est spécifiée, utiliser la date d'aujourd'hui par défaut
    today = datetime.today().strftime('%Y-%m-%d')
    if not date_debut and not date_fin:
        date_debut = today
        date_fin = today

    # Construire la requête SQL avec tri par id_releve
    sql_query = '''
        SELECT 
            r.*, e.libelle_ens, e.lib_plus_ens, z.libelle_zn, z.lib_plus_zn, 
            et.lib_etat_rel, COALESCE(c.nb_article, 0) AS nb_article
        FROM rel_index_releve r
        JOIN rel_enseigne e ON r.enseigne_releve = e.enseigne_ens
        JOIN rel_zone_prix z ON r.zone_releve = z.zone_zn
        JOIN rel_etat et ON r.etat_rel = et.rel_etat_code
        LEFT JOIN (
            SELECT num_rel_rel, COUNT(*) AS nb_article
            FROM rel_releve
            GROUP BY num_rel_rel
        ) c ON r.id_releve = c.num_rel_rel
        WHERE 1=1
    '''
    
    params = []
    if concurrent:
        sql_query += ' AND r.enseigne_releve = %s'
        params.append(concurrent)
    
    if date_debut and date_fin:
        sql_query += ' AND r.date_releve BETWEEN %s AND %s'
        params.extend([date_debut, date_fin])
    elif date_debut:
        sql_query += ' AND r.date_releve >= %s'
        params.append(date_debut)
    elif not date_debut and date_fin >= today:
        date_debut = today
        date_fin = today
        sql_query += ' AND r.date_releve BETWEEN %s AND %s'
        params.extend([date_debut, date_fin])
    elif not date_debut and date_fin < today:
        date_debut = 'null'
        date_fin = 'null'
        sql_query += ' AND r.date_releve BETWEEN %s AND %s'
        params.extend([date_debut, date_fin])

    # Ajouter la clause ORDER BY pour trier par id_releve
    sql_query += ' ORDER BY r.id_releve'

    # Exécuter la requête SQL
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query, params)
        rows = cursor.fetchall()
        description = cursor.description

    # Vérifie si la requête retourne des résultats
    if description is None:
        return JsonResponse({'data': [], 'error': 'No results found'}, safe=False)

    # Construire le résultat au format JSON
    columns = [col[0] for col in description]
    results = [dict(zip(columns, row)) for row in rows]
    
    return JsonResponse({'data': results}, safe=False)


# ----------------------------------Insertion noiveau relevé------------------------------------------------------------------------
@csrf_exempt
def ajout_releve(request):
    """Ajoute un nouveau relevé à la base de données."""
    if request.method == 'POST':
        try:
            enseigne_id = request.POST.get('enseigne')
            zone_id = request.POST.get('zone')
            nom_releve = request.POST.get('nom_releve')
            personnel = select_by_id_personnel(request.session.get('nummatr'))

            if not nom_releve:
                return JsonResponse({'success': False, 'message': 'Choisir un nom de relevé.'})

            # Obtenir les instances de Enseigne et Zone
            enseigne_instance = get_object_or_404(Enseigne, pk=enseigne_id)
            zone_instance = get_object_or_404(Zone, pk=zone_id)
                
            # Création de l'objet IndexReleve
            id = IndexReleve.objects.create(
                enseigne_releve=enseigne_instance,
                zone_releve=zone_instance,
                libelle_releve=nom_releve,
                date_releve=request.POST.get('date_creation'),
                lib_plus_releve=request.POST.get('autre_info'),
                dt_maj_releve=datetime.now(),
                dt_trans_releve=datetime.now(),
                etat_rel=4,
            )
            data = [
                (request.session.get('nummatr'), "Creation relevé", f'{personnel[1]} {personnel[2]} a inséré des nouvel releve numero:{id.id_releve}')
            ]
            historique(data)
            

            return JsonResponse({'success': True, 'message': 'Relevé ajouté avec succès !'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur lors de l\'ajout de relevé : {e}'})
    else:
        return JsonResponse({'success': False, 'message': 'Requête invalide.'})



# ----------------------------------Suppression relevé------------------------------------------------------------------------
@csrf_exempt
def delete_releve(request):
    """Supprime un relevé de la base de données."""
    if request.method == 'POST':
        id = request.POST.get('id')
        personnel = select_by_id_personnel(request.session.get('nummatr'))
        
        
        # Vérifie si l'ID est fourni
        if not id:
            return JsonResponse({'success': False, 'message': 'ID non fourni.'})
        
        try:
            # Récupère l'objet à supprimer
            releve = get_object_or_404(IndexReleve, id_releve=id)
            
            # Supprime l'objet
            releve.delete()
            data = [
                (request.session.get('nummatr'), "Suppession ", f"{personnel[1]} {personnel[2]} a supprimé le releve numero : {id} ")
            ]
            historique(data)
            
            return JsonResponse({'success': True, 'message': 'Relevé supprimé avec succès.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur lors de suppression de relevé : {e}'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})



# --------------------------------------Update informationpar article concurrent----------------------------------------------------------------------
@csrf_exempt
def update_etat_releve(request):
    if request.method == 'POST':
        numero = request.POST.get('num')
        etat = int(request.POST.get('etat', 0))  # Conversion directe en entier avec valeur par défaut

        try:
            if etat in [3, 4]:  # Regrouper les deux états
                personnel = select_by_id_personnel(request.session.get('nummatr'))
                index_releve = get_object_or_404(IndexReleve, id_releve=numero, etat_rel=etat)
                
                index_releve.dt_maj_releve = datetime.now()
                index_releve.dt_trans_releve = datetime.now()
                index_releve.etat_rel = 1 if etat == 3 else 0  # État à 1 si etat == 3, sinon 0
                index_releve.save()

                message = f"{personnel[1]} {personnel[2]} a modifié l'état de l'index releve numéro : {numero}"
                historique([(request.session.get('nummatr'), "Mis à jour", message)])
                
                etat_label = "en attente" if etat == 3 else "chargeable"
                return JsonResponse({'success': True, 'message': f'État modifié {etat_label} avec succès.'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur lors de la modification de l\'état : {e}'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})

# --------------------------------------Select by id releve----------------------------------------------------------------------
@csrf_exempt
def select_by_id_releve(request):
    id_releve = request.POST.get('id_releve')
    
    # Utilisation de paramètres SQL pour éviter l'injection SQL
    sql_query = '''
        SELECT * FROM rel_index_releve
        WHERE id_releve = %s
    '''
    
    # Exécuter la requête SQL
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query, [id_releve])
        rows = cursor.fetchall()

        # Convertir les résultats en une liste de dictionnaires
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

    return JsonResponse({'data': results}, safe=False)





# --------------------------------------Update information par article concurrent----------------------------------------------------------------------
@csrf_exempt
def update_etat_releve_and_index(request):
    if request.method == 'POST':
        numero = request.POST.get('num_rel_rel')
        try:
            personnel = select_by_id_personnel(request.session.get('nummatr'))
            # Utilisation d'une transaction atomique
            with transaction.atomic():
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Mise à jour des enregistrements dans la table rel_releve
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE rel_releve
                        SET dt_maj_releve = %s,
                            date_val_releve = %s,
                            etat_rel = 2
                        WHERE num_rel_rel = %s
                    """, [current_time, current_time, numero])

                # Mise à jour de l'enregistrement dans la table rel_index_releve
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE rel_index_releve
                        SET dt_maj_releve = %s,
                            dt_trans_releve = %s,
                            etat_rel = 2
                        WHERE id_releve = %s
                    """, [current_time, current_time, numero])
            data = [
                (request.session.get('nummatr'), "Mis a jour ", f"{personnel[1]} {personnel[2]} a modifier l'etat de rel_rel index numero : {numero} ")
            ]
            historique(data)

            return JsonResponse({'success': True, 'message': 'État modifié avec succès.'})
        except Exception as e:
            print(f"Erreur : {e}")
            return JsonResponse({'success': False, 'message': f'Erreur lors de la modification de l\'état : {e}'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})


