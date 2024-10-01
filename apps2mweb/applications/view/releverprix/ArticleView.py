from django.db import   connections
from django.http import JsonResponse
from applications.view.releverprix import RelReleveView
from django.db import transaction
from applications.view.releverprix.PersonnelPView import select_by_id_personnel
from applications.view.releverprix.RayonView import select_all_rayon
from applications.view.releverprix.RelLogView import historique
from applications.view.releverprix.ZoneView import select_by_id_zone
from applications.view.releverprix.helper.manage_index import manage_indexes_releve, manage_releve_existing
from django.views.decorators.csrf import csrf_exempt

#--------------------------Filtration des articles ----------------------
@csrf_exempt
def applique_filtre_article_s2m(request):
    fournisseur = request.POST.get('fournisseur')
    rayon = request.POST.get('rayon')
    gencode_reference = request.POST.get('gencode')  # Gencode ou référence

    if not fournisseur and not rayon and not gencode_reference:
        return JsonResponse({'data': []}, safe=False)

    # Étape 1: Requête SQL PostgreSQL avec jointures
    sql_query_postgres = '''
        SELECT 
            a.art, a.*, f.raison_social_frs, r.rayl30c, r.sectray, p.deb_pv, p.prix_pv, p.pvht_pv, p.tva_pv
        FROM article a
        LEFT JOIN fournisseur f ON a.fn = f.id_frs
        LEFT JOIN rayon r ON a.ray = r.rayon
        LEFT JOIN pvn_ref p ON a.art = p.art_pv
        WHERE 1=1
    '''
    params_postgres = []
    if fournisseur:
        sql_query_postgres += ' AND a.fn = %s'
        params_postgres.append(fournisseur)
    if rayon:
        sql_query_postgres += ' AND a.ray = %s'
        params_postgres.append(rayon)
    if gencode_reference:
        sql_query_postgres += ' AND (CAST(a.gencod AS TEXT) = %s OR CAST(a.art AS TEXT) = %s)'  # Comparaison en tant que chaîne
        params_postgres.append(gencode_reference)
        params_postgres.append(gencode_reference)

    with connections['sifaka-postgres'].cursor() as cursor:
        cursor.execute(sql_query_postgres, params_postgres)
        postgres_rows = cursor.fetchall()
    postgres_columns = [col[0] for col in cursor.description]
    postgres_results = [dict(zip(postgres_columns, row)) for row in postgres_rows]

    # Étape 2: Requête SQL MySQL pour `rel_art_concur`
    sql_query_mysql = '''
        SELECT 
            ref_ac, count(ref_ac) as article_rattache
        FROM rel_art_concur
        GROUP BY ref_ac
    '''
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query_mysql)
        mysql_rows = cursor.fetchall()
    mysql_results = {row[0]: row[1] for row in mysql_rows}  # Dictionnaire avec ref_ac comme clé

    # Étape 3: Fusionner les résultats
    for result in postgres_results:
        art = result['art']
        if art in mysql_results:
            result['article_rattache'] = mysql_results[art]
            result['ref_ac'] = art  # Ajout de `ref_ac`
        else:
            result['article_rattache'] = 0  # Ou une autre valeur par défaut
            result['ref_ac'] = art  # Ajout de `ref_ac` même si aucune correspondance trouvée

    return JsonResponse({'data': postgres_results}, safe=False)



#-------------------------- Selecter tout les articles ----------------------
def select_all_article(request, nomenclature):
    # Liste des colonnes acceptables pour éviter les injections SQL

    # Utiliser le gestionnaire de connexions spécifique à la base de données 'sifaka'
    with connections['sifaka-postgres'].cursor() as cursor:
        # Construire la requête SQL avec le filtrage sur nomenclature
        query = f"""
        SELECT DISTINCT({nomenclature}) FROM article
        ORDER BY {nomenclature} ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Convertir les résultats en une liste de dictionnaires
        columns = [col[0] for col in cursor.description]
        articles = [dict(zip(columns, row)) for row in rows]

    return articles

#-------------------------- Selecter tout les articles ----------------------
@csrf_exempt
def applique_filtre_nomenclature(request):
    nomenclature = request.POST.get('nomenclature')
    if nomenclature == 'ray':
        return JsonResponse({'data': select_all_rayon(request)}, safe=False)
    else:
        return JsonResponse({'data': select_all_article(request,nomenclature)}, safe=False)
       
       
       
        

#-------------------------- Selection des articles filtrer ----------------------
def alimefiltermod(request, critere, filtre, mag):
    with connections['sifaka-postgres'].cursor() as cursor:
        query = f"""
            SELECT * 
            FROM article AS ra
            LEFT JOIN pvmag ON ra.art = pvmag.art_pv
            LEFT JOIN pvn_ref AS pf ON ra.art = pf.art_pv
            WHERE {critere} = '{filtre}' AND mag_pv = '{mag}'
        """         
        cursor.execute(query, [filtre, mag])
        rows = cursor.fetchall()

    # Optionnel: Conversion en dictionnaire pour un retour JSON si nécessaire
    column_names = [col[0] for col in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    return data




#-------------------------- Selection des articles filtrer ----------------------
def alimefiltermodimport(request, ref, mag):
    with connections['sifaka-postgres'].cursor() as cursor:
        query = """
            SELECT * 
            FROM article AS ra
            LEFT JOIN pvmag ON ra.art = pvmag.art_pv
            LEFT JOIN pvn_ref AS pf ON ra.art = pf.art_pv
            WHERE ra.art = %s AND pvmag.mag_pv = %s
        """
        
        cursor.execute(query, [ref, mag])
        rows = cursor.fetchall()
        
        # Optionnel: Conversion en dictionnaire pour un retour JSON si nécessaire
        column_names = [col[0] for col in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]

    return data
    
        

#-------------------------- Ajouter des articles dans le relever ----------------------
@csrf_exempt
def ajout_article(request): 
    resultat = alimefiltermod(request, request.POST.get('critere'), request.POST.get('filtre'), request.POST.get('mag'))
    if not isinstance(resultat, list):
        return JsonResponse({'data': 'Aucun article trouvé'}, safe=False)

    try:
        personnel = select_by_id_personnel( request.session.get('nummatr'))
        
        # Créer les index avant l'insertion
        manage_releve_existing('create')
        manage_indexes_releve('create')
        
        with transaction.atomic():
            data = []
            for element in resultat:
                if isinstance(element, dict):
                    zone_id = request.POST.get('zone')
                    zone_label = select_by_id_zone(request, zone_id)
                    
                    # exist = RelReleveView.check_existing_article(element.get('art'), element.get('gencod'), element.get('lib'),request.POST.get('enseigne'))
                    # if not exist:
                    releve_data = (
                            request.POST.get('num_releve'), 
                            element.get('lib'), 
                            element.get('art'), 
                            element.get('gencod'), 
                            element.get('prix_pv'),
                            element.get('prix_pv'), 
                            zone_id, 
                            zone_label,
                            0, '-', 0, 0, 0
                        )
                    data.append(releve_data)
            
            if data:
                RelReleveView.insertion_releve(data)
        
        # Mise à jour dans une transaction séparée
        for element in resultat:
            if isinstance(element, dict):
                RelReleveView.update_rel_releve(request.POST.get('enseigne'), element.get('art'),request.POST.get('num_releve'))
        # Log the operation
        data_log = [
            (request.session.get('nummatr'), "Insertion", f"{personnel[1]} {personnel[2]} a inséré des nouveaux articles par critère"),
            (request.session.get('nummatr'), "Modification", f"{personnel[1]} {personnel[2]} a modifié des articles")
        ]
        historique(data_log)

        # Supprimer les index après l'insertion
        manage_releve_existing('drop')
        manage_indexes_releve('drop')
        
        return JsonResponse({'success': True, 'message': 'Article inséré avec succès'})

        # return JsonResponse({'data': 'Article inséré avec succès'}, safe=False)
    
    except Exception as e:
        print(e)  # Useful for debugging
        return JsonResponse({'danger': False, 'message': f'Erreur lors de l\'insertion des articles: {str(e)}'})
        # return JsonResponse({'data': f'Erreur lors de l\'insertion des articles: {str(e)}'}, safe=False)
