import os
from django.conf import settings
from django.db import connections

# Récupérer toutes les images associées à un id_art_concur
def get_image_urls_concurrent(id_art_concur):
    # Rechercher les images dans la base de données via SQL direct
    query = "SELECT image_art FROM rel_art_image WHERE id_art_concur = %s"
    params = [id_art_concur]

    try:
        with connections['default'].cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()  # Récupérer toutes les lignes
        
        # Retourner les images si trouvées, sinon None
        return [row[0] for row in rows] if rows else []  # Retourner toutes les images ou une liste vide
    except Exception as e:
        # Afficher l'erreur avec des détails
        print(f"Erreur lors de la récupération des images: {e}")
        return []

def get_image_urls_concurrent_verif(id_art_concur):
    # Rechercher toutes les images associées à un id_art_concur
    images = get_image_urls_concurrent(id_art_concur)
    verified_images = []

    for image in images:
        image_name = f'{image}.png'
        image_path = os.path.join(settings.BASE_DIR, 'applications/static', 'img', 'Nouveau_article', image_name)
        if os.path.exists(image_path):
            verified_images.append(f'/static/img/Nouveau_article/{image_name}')
    
    # Si aucune image n'est trouvée, ajouter une image par défaut
    if not verified_images:
        verified_images.append('/static/img/Nouveau_article/vide.png')

    return verified_images

# # Vérifier si l'image existe dans le répertoire et retourner l'URL correspondante
# def get_image_url_verif(id_art_concur):
#     images = get_image_urls_concurrent(id_art_concur)
#     for image in images:
#         image_name = f'{image}.png'  # Ajout de l'extension .png
#         image_path = os.path.join(settings.BASE_DIR, 'applications/static', 'img', 'Nouveau_article', image_name)
#         print(f"Vérification du chemin : {image_path}")
        
#         # Si l'image existe dans le répertoire, retourner son chemin
#         if os.path.exists(image_path):
#             return f'/static/img/Nouveau_article/{image_name}'
    
#     # Si aucune des images ne correspond, retourner une image par défaut
#     return '/static/img/Nouveau_article/vide.png'  # Image par défaut
