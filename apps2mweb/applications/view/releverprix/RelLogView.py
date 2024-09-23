from django.db import connections, OperationalError, DatabaseError
from datetime import datetime

# -------------------------------------- Insertion des historiques ----------------------------------------------------------------------
def historique(data):
    try:
        with connections['default'].cursor() as cursor:
            # Requête d'insertion SQL
            insert_query = '''
                INSERT INTO rel_log (
                    rel_users, rel_log_action, rel_log_description, rel_log_date
                ) VALUES (%s, %s, %s, %s)
            '''
            
            # Préparation des valeurs à insérer
            values = [
                (
                    rel_users, rel_log_action, rel_log_description, datetime.now()
                )
                for (rel_users, rel_log_action, rel_log_description) in data
            ]
            
            # Exécution de la requête d'insertion
            cursor.executemany(insert_query, values)
            print(f"{len(values)} enregistrements insérés avec succès dans la table rel_log.")
            
    except OperationalError as e:
        # Erreur liée à la connexion ou à l'opération de la base de données
        print("Erreur opérationnelle lors de l'insertion dans la base de données :", e)
        
    except DatabaseError as e:
        # Erreur générale liée à la base de données
        print("Erreur de base de données lors de l'insertion :", e)
        
    except Exception as e:
        # Gestion des autres exceptions
        print("Erreur inconnue lors de l'insertion :", e)
