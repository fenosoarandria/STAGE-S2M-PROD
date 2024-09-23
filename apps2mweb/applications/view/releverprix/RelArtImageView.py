import os
from django.conf import settings
from django.db import connections

def get_image_url(ref_rel):
    # Rechercher l'image dans la base de données via SQL direct
    query = "SELECT image_art FROM rel_art_image WHERE id_art_concur = %s"
    params = [ref_rel]

    try:
        with connections['default'].cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
        
        # Retourner les informations de l'image si trouvée
        return row
    except Exception as e:
        # Afficher l'erreur avec des détails
        print(f"Erreur lors de la récupération de l'image: {e}")
        return None
