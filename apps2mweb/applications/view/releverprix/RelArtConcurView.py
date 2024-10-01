from django.db import transaction
from django.db import connections
from django.http import JsonResponse
from datetime import datetime
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from applications.model.releverprix.base_mysql.RelArtConcur import RelArtConcur
from applications.view.releverprix import RelReleveView
from applications.view.releverprix.PersonnelPView import select_by_id_personnel
from applications.view.releverprix.RelArtImageView import  get_image_urls_concurrent_verif
from applications.view.releverprix.RelLogView import historique
from applications.view.releverprix.ZoneView import select_by_id_zone
from applications.view.releverprix.helper.manage_index import  manage_indexes_rattachement, manage_indexes_releve
from django.db import connections, transaction
import os
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# --------------------------------------Selecter by reference article concurrent ----------------------------------------------------------------------
@csrf_exempt
def select_by_ref_art_concu(request):
    id = request.POST.get('ref')
    # Vérifie si tous les paramètres sont null
    if not id:
        return JsonResponse({'data': []}, safe=False)
    
    sql_query = '''
       SELECT r.*,e.libelle_ens 
            FROM rel_art_concur r
            JOIN rel_enseigne e ON r.enseigne_ac = e.enseigne_ens
                WHERE r.ref_ac = %s
        '''
    params = [id]
    
    # Exécuter la requête SQL
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query, params)
        rows = cursor.fetchall()
        description = cursor.description

    # Vérifie si la requête retourne des résultats
    if not rows:
        return JsonResponse({'data': [], 'error': 'No results found'}, safe=False)

    # Construire le résultat au format JSON
    columns = [col[0] for col in description]
    results = [dict(zip(columns, row)) for row in rows]
    
    return JsonResponse({'data': results}, safe=False)


# -------------------------------------- Filtration des articles concurren ----------------------------------------------------------------------


@csrf_exempt
def filtre_article_concurrent(request):
    enseigne = request.POST.get('ens_id')
    rattachement = request.POST.get('rattachement')

    # Requête SQL pour obtenir les articles concurrents filtrés
    sql_query = '''
    SELECT 
        c.id_art_concur,
        c.enseigne_ac,
        r.ref_rel,
        c.libelle_ac AS lib_art_concur_rel,
        c.gencod_ac AS gc_concur_rel,
        r.prix_concur_rel,
        c.etat AS statut_rattachement,
        rel_enseigne.libelle_ens
    FROM 
        rel_releve r
    JOIN 
        rel_art_concur c ON r.ref_rel = c.ref_ac
    JOIN 
        rel_enseigne ON c.enseigne_ac = rel_enseigne.enseigne_ens
    WHERE 
        c.enseigne_ac = %s AND c.etat = %s
    '''

    try:
        with connections['default'].cursor() as cursor:
            cursor.execute(sql_query, [enseigne, rattachement])
            rows = cursor.fetchall()

            # Colonnes de la requête SQL
            columns = [col[0] for col in cursor.description]
            results = []

            # Parcourir les résultats pour ajouter l'URL de l'image
            for row in rows:
                result_dict = dict(zip(columns, row))
                # Appel à la fonction pour vérifier l'image (récupérer plusieurs images)
                result_dict['images'] = get_image_urls_concurrent_verif(result_dict['id_art_concur'])
                results.append(result_dict)

        return JsonResponse({'data': results}, safe=False)
    except Exception as e:
        print(f"Erreur lors de la récupération des articles concurrents: {e}")
        return JsonResponse({'error': 'Erreur lors de la récupération des données'}, status=500)



# -------------------------------------- Select relever art concur by id enseigne ----------------------------------------------------------------------
def get_rel_art_concur_data(enseigne_ac):
    query = '''
        SELECT * 
        FROM rel_art_concur 
        WHERE enseigne_ac = %s AND etat = 1
    '''
    with connections['default'].cursor() as cursor:
        cursor.execute(query, [enseigne_ac])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]        
        # Convertir les lignes en une liste de dictionnaires
        data = [dict(zip(columns, row)) for row in rows] 
    return data
 
 
 
# -------------------------------------- Insertion article concurrent ----------------------------------------------------------------------
def insertion_rel_art_concur(data):
    inserted_ids = []
    
    with connections['default'].cursor() as cursor:
        # Préparer la requête d'insertion
        insert_query = '''
            INSERT INTO rel_art_concur (
                enseigne_ac, ref_ac, libelle_ac, gencod_ac, etat, date_maj, user_maj
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        
        for row in data:
            enseigne_ac, ref_ac, libelle_ac, gencod_ac, etat, user_maj = row
            
            cursor.execute(insert_query, (
                enseigne_ac, ref_ac, libelle_ac, gencod_ac, etat, datetime.now(), user_maj
            ))
            
            # Obtenir l'ID de la ligne insérée
            inserted_id = cursor.lastrowid
            inserted_ids.append(inserted_id)
    
    return inserted_ids
    
# -------------------------------------- Rattachement des articles concurrent ----------------------------------------------------------------------
@csrf_exempt
def ajout_rattachement_concurrent(request):
    if request.method == 'POST':
        try:
            personnel = select_by_id_personnel(request.session.get('nummatr'))
            
            # Replacer l'ordre des champs correctement
            data = [
                (request.POST.get('enseigne'), request.POST.get('reference'), request.POST.get('libelle'), request.POST.get('gencode'), 1, request.session.get('nummatr')),
            ]
            insertion_rel_art_concur(data)
            RelReleveView.update_rel_releve_etat_rattachement(request.POST.get('reference'),request.POST.get('gencode_s2m'))
            data = [
                (request.session.get('nummatr'), "Ajout ", f" {personnel[1]} {personnel[2]} a ajouter des rattachement")
            ]
            historique(data)
            return JsonResponse({'success': True, 'message': 'Article rattaché avec succès !'})

        except Exception as e:
            # Log de l'exception pour le diagnostic
            print(f'Erreur lors de rattachement d\'un article : {str(e)}')
            return JsonResponse({'success': False, 'message': f'Erreur lors de rattachement d\'un article : {str(e)}'})
    else:
        return JsonResponse({'success': False, 'message': 'Requête non valide.'})



# -------------------------------------- Import rattachement des articles concurrent ----------------------------------------------------------------------
@csrf_exempt
def import_rattachement_concurrent_exel(request):
    personnel = select_by_id_personnel(request.session.get('nummatr'))
    
    if request.method != 'POST':
        return JsonResponse({'data': 'Méthode non autorisée'}, status=405)
    
    excel_file = request.FILES.get('importExcelRattachement')
    if not excel_file:
        return JsonResponse({'data': 'Aucun fichier reçu'}, status=400)
    
    file_extension = excel_file.name.split('.')[-1].lower()
    try:
        # Lire le fichier sans en-tête
        if file_extension == 'csv':
            df = pd.read_csv(excel_file, header=None)
        elif file_extension in ['xls', 'xlsx']:
            df = pd.read_excel(excel_file, header=None)
        else:
            return JsonResponse({'data': 'Format de fichier non pris en charge'}, status=400)

        df.columns = ['NUMERO_ENSEIGNE', 'REF_S2M', 'LIB_CONC', 'GEN_CONC']
        data = df[['NUMERO_ENSEIGNE', 'REF_S2M', 'LIB_CONC', 'GEN_CONC']].fillna('')
        
        num_rows = len(data)

        manage_indexes_rattachement('create')  # Créer les index avant l'insertion

        with transaction.atomic():
            batch_data = []
            for _, row in data.iterrows():
                if not check_existing_article_concurrent(row['NUMERO_ENSEIGNE'], row['REF_S2M'], row['LIB_CONC'], row['GEN_CONC']):
                    batch_data.append((
                        row['NUMERO_ENSEIGNE'], row['REF_S2M'], row['LIB_CONC'], 
                        row['GEN_CONC'], 1, request.session.get('nummatr') # Remplacez 'user' par l'utilisateur réel si disponible
                    ))
            insertion_rel_art_concur(batch_data)  # Insérer en lot pour améliorer la performance
            
            data = [
                (request.session.get('nummatr'), "Ajout ", f" {personnel[1]} {personnel[2]} a ajouter des rattachements par importatione exel")
            ]
            historique(data)
        manage_indexes_rattachement('drop')  # Supprimer les index après l'insertion
        return JsonResponse({'success': True, 'message': 'Fichier importé avec succès.'})
    except Exception as e:
        return JsonResponse({'danger': False, 'message': f'Erreur lors de l\'importation: {str(e)}'})
    
    
# -------------------------------------- Import rattachement des articles concurrent ----------------------------------------------------------------------
@csrf_exempt
def import_rattachement_s2m_en_concurrent_exel(request):
    personnel = select_by_id_personnel(request.session.get('nummatr'))
    
    if request.method != 'POST':
        return JsonResponse({'data': 'Méthode non autorisée'}, status=405)
    
    excel_file = request.FILES.get('importExcelRattachementConcurrent')
    if not excel_file:
        return JsonResponse({'data': 'Aucun fichier reçu'}, status=400)
    
    file_extension = excel_file.name.split('.')[-1].lower()
    try:
        # Lire le fichier sans en-tête
        if file_extension == 'csv':
            df = pd.read_csv(excel_file, header=None)
        elif file_extension in ['xls', 'xlsx']:
            df = pd.read_excel(excel_file, header=None)
        else:
            return JsonResponse({'data': 'Format de fichier non pris en charge'}, status=400)

        df.columns = ['NUMERO_ENSEIGNE', 'REF_S2M', 'LIB_CONC', 'GEN_CONC']
        data = df[['NUMERO_ENSEIGNE', 'REF_S2M', 'LIB_CONC', 'GEN_CONC']].fillna('')
        
        manage_indexes_rattachement('create')  # Créer les index avant l'insertion

        with transaction.atomic():
            for _, row in data.iterrows():
                
                # Si l'article n'existe pas, insérer
                id_art_concur = update_rattachement_s2m_concurrent(row['NUMERO_ENSEIGNE'], row['REF_S2M'],row['GEN_CONC'])
                RelReleveView.update_rel_releve_etat_rattachement_nouveau(id_art_concur)

            data = [
                (request.session.get('nummatr'), "Ajout ", f" {personnel[1]} {personnel[2]} a ajouter des rattachements par importatione exel")
            ]
            historique(data)
        manage_indexes_rattachement('drop')  # Supprimer les index après l'insertion
        return JsonResponse({'success': True, 'message': 'Fichier importé avec succès.'})
    except Exception as e:
        return JsonResponse({'danger': False, 'message': f'Erreur lors de l\'importation: {str(e)}'})
    
    
    
    
    
def update_rattachement_s2m_concurrent(enseigne_ac, reference, gencode):
    with connections['default'].cursor() as cursor:
        # Récupérer l'ID correspondant avant la mise à jour
        cursor.execute("""
            SELECT id_art_concur
            FROM rel_art_concur
            WHERE enseigne_ac = %s 
              AND gencod_ac = %s
        """, [enseigne_ac, gencode])
        id_updated = cursor.fetchone()  # Récupère la première ligne

        # Si un ID est trouvé, faire l'update
        if id_updated:
            cursor.execute("""
                UPDATE rel_art_concur
                SET ref_ac = %s,
                    etat = 1
                WHERE enseigne_ac = %s 
                  AND gencod_ac = %s
            """, [reference, enseigne_ac, gencode])
            
            rows_updated = cursor.rowcount  # Nombre de lignes mises à jour

            # Vérifier si l'update a affecté des lignes
            if rows_updated > 0:
                return id_updated[0]  # Retourne l'ID mis à jour
    
    return None  # Retourne None si aucun ID n'a été trouvé ou mis à jour

# -------------------------------------- Import nouveau concurrent non rattacher ----------------------------------------------------------------------
@csrf_exempt
def import_excel_releve_concurrent(request):
    if request.method != 'POST':
        return JsonResponse({'data': 'Méthode non autorisée'}, status=405)

    excel_file = request.FILES.get('importExcel')
    if not excel_file:
        return JsonResponse({'data': 'Aucun fichier reçu'}, status=400)

    file_extension = excel_file.name.split('.')[-1].lower()
    try:
        personnel = select_by_id_personnel(request.session.get('nummatr'))
        
        # Lire le fichier selon l'extension
        df = pd.read_csv(excel_file, header=0) if file_extension == 'csv' else pd.read_excel(excel_file, header=0)
        if file_extension not in ['csv', 'xls', 'xlsx']:
            return JsonResponse({'data': 'Format de fichier non pris en charge'}, status=400)
        
        # Assigner des noms de colonnes et gérer les valeurs manquantes
        df.columns = ['GENCODE_CONC', 'LIBELLE_ART_CONC', 'PRIX_CONC', 'LIB_PLUS_CONC']
        data = df.fillna('')
        
        manage_indexes_releve('create')
        with transaction.atomic():
            num_releve = request.POST.get('num_releve')
            zone, enseigne = request.POST.get('zone'), request.POST.get('enseigne')
            ref = 499999
            zonelib = select_by_id_zone(request, zone)

            for _, row in data.iterrows():
                ref += 1
                prix_conc = float(str(row['PRIX_CONC']).replace(",", ".")) if row['PRIX_CONC'] else 0.00
                
                # Vérification de l'existence de l'article concurrent
                if not check_existing_article_concurrent(enseigne, ref, row['LIBELLE_ART_CONC'], row['GENCODE_CONC']):
                    # Si l'article n'existe pas, insérer
                    id_art_concur = insertion_rel_art_concur([(enseigne, ref, row['LIBELLE_ART_CONC'], row['GENCODE_CONC'], 0, request.session.get('nummatr'))])
                    
                    RelReleveView.insertion_releve([(num_releve, f"Article : {ref}", ref, f"Gencode : {ref}", 0, 0, zone, zonelib, id_art_concur,
                                       row['LIBELLE_ART_CONC'], row['GENCODE_CONC'], row['LIB_PLUS_CONC'], prix_conc)])
                else:
                    print(f"L'article concurrent {row['LIBELLE_ART_CONC']} avec Gencode {row['GENCODE_CONC']} existe déjà.")
            
            # Historique de l'action
            historique([(request.session.get('nummatr'), "Creation", f"{personnel[1]} {personnel[2]} a ajouté des articles concurrents non rattachés ")])
            manage_indexes_releve('drop')
        return JsonResponse({'success': True, 'message': 'Fichier importé avec succès.'})

        # return JsonResponse({'data': 'Fichier importé avec succès', 'rows': len(data)})

    except Exception as e:
        print(e)
        return JsonResponse({'danger': False, 'message': f'Erreur lors de l\'importation: {str(e)}'})
        # return JsonResponse({'data': f'Erreur lors de l\'importation: {str(e)}'}, status=500)


# -------------------------------------- Verification si un article concurrent existe deja ----------------------------------------------------------------------
def check_existing_article_concurrent(enseigne, ref, libelle, gencode):
    return RelArtConcur.objects.filter(
        enseigne_ac=enseigne,
        ref_ac=ref,
        libelle_ac=libelle,
        gencod_ac=gencode
    ).exists()



# --------------------------------------Select by id article concurrent ----------------------------------------------------------------------
def select_by_id_art_concur(id):
    
    # Utilisation de paramètres SQL pour éviter l'injection SQL
    sql_query = '''
        SELECT * FROM rel_art_concur
        WHERE id_art_concur = %s 
    '''
    # Exécuter la requête SQL
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query, [id])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        if row:
            # Conversion du tuple en dictionnaire
            return dict(zip(columns, row))
        return None


            
@csrf_exempt
def ajout_rattachement_s2m(request):
    if request.method == 'POST':
        try:
            ref = request.POST.get('reference_s2m')
            id = request.POST.get('id_art_concur')
            
            
            # Appel de la méthode pour récupérer la référence
            reference = RelReleveView.select_by_reference(ref)
            if reference is None:
                return JsonResponse({'danger': True, 'message': 'Aucun enregistrement trouvé avec la référence donnée.'}, status=404)

            # Préparer les données pour la mise à jour
            data = {
                'libelle_art_rel': reference['libelle_art_rel'],
                'gencod_rel': reference['gencod_rel'],
                'prix_ref_rel': reference['prix_ref_rel'],
                'prix_zone_rel': reference['prix_zone_rel']
            }
            
            # Utiliser une transaction pour garantir la cohérence des mises à jour
            with transaction.atomic():
                # Récupération des attributs S2M et des concurrents
                concurrent_attributs = RelArtConcur.objects.filter(id_art_concur=id)
                
                # Appel de la fonction pour mettre à jour les enregistrements
                RelReleveView.update_s2m_attributs(ref, data, id, faux_ref=concurrent_attributs.first().ref_ac if concurrent_attributs.exists() else None)

                # Mettre à jour les enregistrements trouvés pour les concurrents
                for concurrent_attribut in concurrent_attributs:
                    concurrent_attribut.ref_ac = ref
                    concurrent_attribut.etat = 1
                    concurrent_attribut.date_maj = datetime.now()
                    concurrent_attribut.save()

            # Récupérer les informations du personnel pour le log
            personnel = select_by_id_personnel(request.session.get('nummatr'))
            if personnel:
                data = [
                    (request.session.get('nummatr'), "Ajout", f"{personnel[1]} {personnel[2]} a ajouté des rattachements")
                ]
                historique(data)

            return JsonResponse({'success': True, 'message': 'Article rattaché avec succès!'})

        except Exception as e:
            # Log de l'exception pour le diagnostic
            print(f'Erreur lors du rattachement d\'un article : {str(e)}')
            return JsonResponse({'danger': True, 'message': f'Erreur lors du rattachement d\'un article : {str(e)}'}, status=500)

    else:
        return JsonResponse({'danger': True, 'message': 'Requête non valide.'}, status=405)
