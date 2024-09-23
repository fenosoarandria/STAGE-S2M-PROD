from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connections


# --------------------------------------Selecter tout les articles ----------------------------------------------------------------------
def get_article_data(ref_rel):
    article_data = {}

    with connections['sifaka-postgres'].cursor() as cursor:
        cursor.execute('''
            SELECT ray
            FROM article 
            WHERE art = %s
        ''', [ref_rel])
        
        row = cursor.fetchone()
        if row:
            article_data = {'ray': row[0]}
    
    return article_data



# --------------------------------------Filtre des recap ----------------------------------------------------------------------
@csrf_exempt
def applique_filtre_recap(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. POST required.'}, status=405)

    date_debut = request.POST.get('date_debut')
    date_fin = request.POST.get('date_fin')
    ref_or_gencode = request.POST.get('ref_rel_recap_gencode')  # Utilisation du même input pour ref_rel ou gencode

    if not date_debut and not date_fin and not ref_or_gencode:
        return JsonResponse({'data': []}, safe=False)

    # Étape 2: Récupération des données MySQL avec filtrage par dates, référence ou gencode
    sql_query = '''
        SELECT r.*, ri.*, en.*, r.*
        FROM rel_releve r
        LEFT JOIN rel_index_releve ri ON r.num_rel_rel = ri.id_releve
        LEFT JOIN rel_enseigne en ON ri.enseigne_releve = en.enseigne_ens
        WHERE 1=1
    '''
    params = []

    # Filtrer par référence ou gencode
    if ref_or_gencode:
        sql_query += ' AND (r.ref_rel = %s OR r.gencod_rel = %s)'
        params.extend([ref_or_gencode, ref_or_gencode])

    # Filtrer par dates si fournies
    if date_debut and date_fin:
        sql_query += ' AND r.date_rel BETWEEN %s AND %s'
        params.extend([date_debut, date_fin])
    elif date_debut:
        sql_query += ' AND r.date_rel >= %s'
        params.append(date_debut)
    elif date_fin:
        sql_query += ' AND r.date_rel <= %s'
        params.append(date_fin)

    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query, params)
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse({'data': [], 'error': 'No results found'}, safe=False)

        columns = [col[0] for col in cursor.description]
        data = []

        for row in rows:
            entry = dict(zip(columns, row))
            ref_rel = entry['ref_rel']            
            # Récupérer les données de l'article
            article_data = get_article_data(ref_rel)
            entry['article_data'] = article_data
            data.append(entry)

    return JsonResponse({'data': data}, safe=False)
