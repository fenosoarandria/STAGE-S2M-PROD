
from django.db import connections


#-------------------------- Selecter tout les rayon  ----------------------
def select_all_rayon(request):
    # Utiliser le gestionnaire de connexions spécifique à la base de données 'sifaka'
    with connections['sifaka'].cursor() as cursor:
        cursor.execute("SELECT * FROM rayon")
        rows = cursor.fetchall()

    # Convertir les résultats en une liste de dictionnaires
    columns = [col[0] for col in cursor.description]
    rayon = [dict(zip(columns, row)) for row in rows]

    return rayon

