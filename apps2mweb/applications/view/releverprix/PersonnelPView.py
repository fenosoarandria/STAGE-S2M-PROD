from django.db import connections


def select_by_id_personnel(matricule):
    sql_query = '''
    SELECT nummatr,nomcomplet,prenom FROM personnel_p 
        WHERE 
        nummatr = %s
    '''
    params = [matricule] 
    # Exécuter la requête SQL
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query, params)
        rows = cursor.fetchone()    
    return rows