from datetime import datetime, timezone
from django.db import connections
from django.http import JsonResponse
from applications.model.releverprix.base_mysql.RelReleve import RelReleve
from django.db import transaction
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from applications.view.releverprix import ArticleView
from applications.view.releverprix.PersonnelPView import select_by_id_personnel
from applications.view.releverprix.RelLogView import historique
from applications.view.releverprix.helper.manage_index import  manage_indexes_releve


# ----------------------------------Selection de relevé par id------------------------------------------------------------------------
@csrf_exempt
def select_by_id_releve_index(request):
    id = request.POST.get('id')
    # Vérifie si tous les paramètres sont null
    if not id:
        return JsonResponse({'data': []}, safe=False)
    
    sql_query = '''
        SELECT * FROM rel_releve r JOIN rel_etat et ON r.etat_rel = et.rel_etat_code JOIN rel_etat_art eta ON r.etat_sup_conc = eta.code_rel_sup
        WHERE 
        r.num_rel_rel = %s ORDER BY r.ref_rel ASC
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



# ----------------------------------Selection de relevé par reference------------------------------------------------------------------------
@csrf_exempt
def select_by_ref_releve_index(request):
    ref_rel = request.POST.get('ref_rel')
    id_rel_rel = request.POST.get('id_rel_rel')
    num_rel_rel = request.POST.get('num_rel_rel')
    # Concaténation directe des valeurs dans la requête SQL (moins sécurisé)
    sql_query = f'''
        SELECT * FROM rel_releve
        JOIN rel_index_releve ON rel_releve.num_rel_rel = rel_index_releve.id_releve
        JOIN rel_enseigne ON rel_index_releve.enseigne_releve = rel_enseigne.enseigne_ens
        WHERE id_rel_rel = '{id_rel_rel}' AND ref_rel = '{ref_rel}' AND num_rel_rel = '{num_rel_rel}'
    '''
    # Exécuter la requête SQL
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Convertir les résultats en une liste de dictionnaires
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

    return JsonResponse({'data': results}, safe=False)


# --------------------------------------Update informationpar article concurrent----------------------------------------------------------------------
@csrf_exempt
def update_information_article_concurrent(request):
    if request.method == 'POST':
        ref = request.POST.get('ref')
        libelle_conc = request.POST.get('libelle')
        gencode_conc = request.POST.get('gencode')
        prix_conc = request.POST.get('prix')
        autre = request.POST.get('autre')

        # Vérifier que tous les paramètres requis sont fournis
        if not all([ref, libelle_conc, gencode_conc, prix_conc]):
            return JsonResponse({'success': False, 'message': 'Tous les champs sont obligatoires.'})

        try:
            personnel = select_by_id_personnel(request.session.get('nummatr'))
            
            # Utiliser une transaction pour garantir la cohérence des mises à jour
            with transaction.atomic():
                # Utiliser filter() pour récupérer tous les objets correspondants
                attributs = RelReleve.objects.filter(ref_rel=ref)
                
                # Vérifiez s'il y a des résultats
                if not attributs.exists():
                    return JsonResponse({'success': False, 'message': 'Aucun enregistrement trouvé avec le ref donné.'})
                
                # Mettre à jour tous les enregistrements trouvés
                for attribut in attributs:
                    attribut.lib_art_concur_rel = libelle_conc
                    attribut.gc_concur_rel = gencode_conc
                    attribut.prix_concur_rel = prix_conc
                    attribut.lib_plus_rel = autre
                    attribut.dt_maj_releve = datetime.now()
                    attribut.save()
            data = [
                (request.session.get('nummatr'), "Mis a jour ", f"{personnel[1]} {personnel[1]} a modifier les prix des articles")
            ]
            historique(data)

            return JsonResponse({'success': True, 'message': 'Information modifiée avec succès.'})
        
        except Exception as e:
            # Retourner une erreur détaillée en cas de problème
            return JsonResponse({'success': False, 'message': f'Erreur lors de la modification des informations : {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})


# -------------------------------------- Historique des releves par article ----------------------------------------------------------------------
@csrf_exempt
def historique_releve_article(request):
    ref_rel = request.POST.get('ref')
    # Concaténation directe des valeurs dans la requête SQL (moins sécurisé)
    sql_query = f'''
        SELECT * FROM rel_releve
        JOIN rel_index_releve ON rel_releve.num_rel_rel = rel_index_releve.id_releve
        JOIN rel_enseigne ON rel_index_releve.enseigne_releve = rel_enseigne.enseigne_ens
        WHERE ref_rel = '{ref_rel}' 
    '''
    # Exécuter la requête SQL
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Convertir les résultats en une liste de dictionnaires
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

    return JsonResponse({'data': results}, safe=False)


# -------------------------------------- Insertion nouveau releve ----------------------------------------------------------------------       
def insertion_releve(data):
    with connections['default'].cursor() as cursor:
        insert_query = '''
            INSERT INTO rel_releve (
                num_rel_rel, date_rel, ref_rel, libelle_art_rel, gencod_rel,
                prix_ref_rel, prix_zone_rel, zone_rel, lib_zn_rel, id_art_conc_rel,
                lib_art_concur_rel, gc_concur_rel, lib_plus_rel, prix_concur_rel,
                dt_maj_releve, date_val_releve
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = [
            (
                num_rel_rel, datetime.now(), ref_rel, libelle_art_rel, gencod_rel,
                prix_ref_rel, prix_zone_rel, zone_rel,lib_zn_rel,id_art_conc_rel,lib_art_concur_rel,gc_concur_rel,lib_plus_rel,prix_concur_rel,
                datetime.now(), datetime.now()
            )
            for (num_rel_rel, libelle_art_rel, ref_rel, gencod_rel, prix_ref_rel, prix_zone_rel, zone_rel,lib_zn_rel,id_art_conc_rel,lib_art_concur_rel,gc_concur_rel,lib_plus_rel,prix_concur_rel) in data
            # for (num_rel_rel, libelle_art_rel, ref_rel, gencod_rel, prix_ref_rel, prix_zone_rel, zone_rel) in data
        ]
        cursor.executemany(insert_query, values)
        return len(values)
    
# -------------------------------------- Modification relever (rattachement des articles deja rattacher ) ----------------------------------------------------------------------
def update_rel_releve(enseigne_ac, reference, num_rel_rel):
    with connections['default'].cursor() as cursor:
        cursor.execute("""
            UPDATE rel_releve
            JOIN rel_art_concur ON rel_releve.ref_rel = rel_art_concur.ref_ac
            SET rel_releve.id_art_conc_rel = rel_art_concur.id_art_concur,
                rel_releve.lib_art_concur_rel = rel_art_concur.libelle_ac,
                rel_releve.gc_concur_rel = rel_art_concur.gencod_ac,
                statut_rattachement = 1
            WHERE rel_art_concur.enseigne_ac = %s 
              AND rel_releve.ref_rel = %s 
              AND rel_releve.num_rel_rel = %s
        """, [enseigne_ac, reference, num_rel_rel])
        
        # Récupérer le nombre de lignes mises à jour
        rows_updated = cursor.rowcount
    
    return rows_updated
        
# -------------------------------------- Modification relever (rattachement des articles deja rattacher ) ----------------------------------------------------------------------
staticmethod     
def update_rel_releve_etat_rattachement(ref_ac,gencode):
    with connections['default'].cursor() as cursor:
        cursor.execute("""
            UPDATE rel_releve
            JOIN rel_art_concur ON rel_releve.ref_rel = rel_art_concur.ref_ac
            SET rel_releve.id_art_conc_rel = rel_art_concur.id_art_concur,
                rel_releve.lib_art_concur_rel = rel_art_concur.libelle_ac,
                rel_releve.gc_concur_rel = rel_art_concur.gencod_ac,
                statut_rattachement = 1
            WHERE rel_releve.ref_rel = %s
            AND rel_releve.gencod_rel = %s
        """, [ref_ac,gencode])


# -------------------------------------- Import exel de releve ----------------------------------------------------------------------
@csrf_exempt
def import_excel_releve(request):
    if request.method != 'POST':
        return JsonResponse({'data': 'Méthode non autorisée'}, status=405)

    excel_file = request.FILES.get('importExcel')
    if not excel_file:
        return JsonResponse({'data': 'Aucun fichier reçu'}, status=400)

    file_extension = excel_file.name.split('.')[-1].lower()
    try:
        personnel = select_by_id_personnel(request.session.get('nummatr'))

        # Lire le fichier selon le format
        df = pd.read_csv(excel_file, header=None) if file_extension == 'csv' else pd.read_excel(excel_file, header=None)
        if file_extension not in ['csv', 'xls', 'xlsx']:
            return JsonResponse({'data': 'Format de fichier non pris en charge'}, status=400)

        df.columns = ['REFERENCE', 'LIBELLE', 'GENCODE']
        data = df.fillna('')

        manage_indexes_releve('create')
        with transaction.atomic():
            num_releve, zone, enseigne, mag = [request.POST.get(k) for k in ['num_releve', 'zone', 'enseigne', 'mag']]
            insertion_data = []

            for _, row in data.iterrows():
                resultat = ArticleView.alimefiltermodimport(request, row['REFERENCE'], mag)
                existing_article = check_existing_article(row['REFERENCE'], row['GENCODE'], row['LIBELLE'], enseigne)
                if not resultat:
                    insertion_data.append((num_releve, row['LIBELLE'], row['REFERENCE'], row['GENCODE'], 0, 0, zone))
                elif not existing_article:
                    #(num,libelle,ref,gen,prix_pv,prix_pv,zone,)
                    insertion_data.extend(
                        (num_releve, row['LIBELLE'], row['REFERENCE'], row['GENCODE'], 
                         element.get('prix_pv', 0), element.get('prix_pv', 0), zone, 0, 0, '-', 0, 0, 0)
                        for element in resultat if isinstance(element, dict)
                    )

            if insertion_data:
                insertion_releve(insertion_data)
            # Mise à jour dans une transaction séparée
        for element in resultat:
            if isinstance(element, dict):
                update_rel_releve(enseigne,row['REFERENCE'],request.POST.get('num_releve'))
        
        
            historique([(request.session.get('nummatr'), "Creation", f"{personnel[1]} {personnel[2]} a ajouté de nouveaux relevés"),
                        (request.session.get('nummatr'), "Mise à jour", f"{personnel[1]} {personnel[2]} a modifié des prix de relevés")])

            manage_indexes_releve('drop')

        return JsonResponse({'data': 'Fichier importé avec succès', 'rows': len(data)})

    except Exception as e:
        return JsonResponse({'data': f'Erreur lors de l\'importation: {str(e)}'}, status=500)
    


# --------------------------------------  Voir si l'article existe deja) ----------------------------------------------------------------------
def check_existing_article(reference, gencode, libelle, enseigne):
    return RelReleve.objects.filter(
        ref_rel=reference,
        gencod_rel=gencode,
        libelle_art_rel=libelle,
        num_rel_rel__enseigne_releve__enseigne_ens=enseigne
    ).exists()
    

def select_by_reference(ref):
    sql_query = '''
        SELECT * FROM rel_releve
        WHERE ref_rel = %s
    '''
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query, [ref])
        # Récupérer le nom des colonnes pour un retour plus structuré
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        if row:
            # Conversion du tuple en dictionnaire
            return dict(zip(columns, row))
        return None
    
def update_s2m_attributs(ref, data, id_concurrent, faux_ref):
    # Récupérer l'instance de la connexion
    with connections['default'].cursor() as cursor:
        # Requête SQL pour la mise à jour
        sql_query = '''
            UPDATE rel_releve
            SET 
                ref_rel = %s,
                libelle_art_rel = %s,
                gencod_rel = %s,
                prix_ref_rel = %s,
                prix_zone_rel = %s,
                dt_maj_releve = %s,
                statut_rattachement = %s
            WHERE ref_rel = %s and id_art_conc_rel = %s
        '''
        
        # Exécution de la requête avec les valeurs du dictionnaire 'data'
        cursor.execute(sql_query, [
            ref,
            data['libelle_art_rel'],   # Libellé de l'article
            data['gencod_rel'],        # Gencode
            data['prix_ref_rel'],      # Prix de référence
            data['prix_zone_rel'],     # Prix par zone
            datetime.now(),            # Date de mise à jour
            1,                         # Statut de rattachement
            faux_ref,
            id_concurrent
        ])

        # Retourner le nombre de lignes affectées
        return cursor.rowcount
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# def check_existing_article(reference, gencode, libelle, enseigne):
#     """
#     Vérifie si l'article avec la référence, le gencode, le libellé et l'enseigne existe déjà 
#     avec toutes les colonnes nécessaires remplies en utilisant une requête SQL brute.
#     Retourne True si toutes les colonnes sont présentes, False sinon.
#     """
#     with connection.cursor() as cursor:
#         query = """
#             SELECT EXISTS (
#                 SELECT 1 FROM rel_releve
#                 JOIN rel_index_releve ON rel_releve.num_rel_rel = rel_index_releve.id_releve
#                 JOIN rel_enseigne ON rel_index_releve.enseigne_releve = rel_enseigne.enseigne_ens
#                 WHERE rel_releve.ref_rel = %s
#                     AND gencod_rel = %s
#                     AND libelle_art_rel = %s
#                     AND rel_enseigne.enseigne_ens = %s
#             )
#         """
#         cursor.execute(query, [reference, gencode, libelle, enseigne])
#         exists = cursor.fetchone()[0]
    
#     return exists
