import json
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.db import connection, OperationalError
from django.http import JsonResponse
from ..ODBCconnect import runQuery 
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def presNam(request, nummatr):
    rows = []
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT nomcomplet, prenom FROM personnel_p WHERE nummatr = %s"
            cursor.execute(sql, [nummatr])
            
            rows = cursor.fetchall()
            print(f"Taille de 'rows': {len(rows)}")
            print(cursor.description)  # Vérifiez la structure des résultats
            for row in rows:
                print(row)  # Afficher chaque ligne récupérée pour vérification

    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")

    return rows  # Retourne les données récupérées
    

def getProduction(request):
    rows = []

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM atb_prod_index")
            rows = cursor.fetchall()
            print(f"Taille de 'rows': {len(rows)}")
            print(cursor.description)  # Vérifiez la structure des résultats
            
            updated_rows = []
            for row in rows:
                print(row[2])  # Afficher chaque ligne récupérée pour vérification
                rows_presNam = presNam(request, row[2])
                print(f"Taille de 'rows' de presNam : {len(rows_presNam)}")
                print(f"Date normalement : {row[1]}")

                # Construire une liste des noms complets des personnes
                personnes_str = []
                for personne in rows_presNam:
                    #personnes_str.append(f"{personne[0]} - {personne[1]}")
                    personnes_str.append(f"{personne[0]}")

                # Mettre à jour row[2] avec toutes les informations récupérées de presNam
                if personnes_str:
                    row_list = list(row)
                    row_list[2] = f"{row_list[2]} - {' / '.join(personnes_str)}"  # Concaténer les noms complets avec '/'
                    updated_row = tuple(row_list)
                    updated_rows.append(updated_row)
                else:
                    updated_rows.append(row)  # Ajouter la ligne inchangée si aucune personne trouvée

    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")

    return updated_rows
    
 # no scence => sabrina carpenter   
@csrf_exempt
def Production(request):
    try:
        tab = []
        production = getProduction(request)
        for row in production: 
            
            try:
                # Vérifier si row[1] est déjà un objet datetime
                if isinstance(row[1], datetime): 
                    date_obj = row[1] 
                else: 
                    # Si row[1] est une chaîne, convertir en objet datetime (optionnel si déjà un datetime)
                    date_obj = datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S")
                
                # Formater la date en chaîne avec le format désiré
                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                #print(f"Voici alors la valeur {formatted_date}")
                
                action = f'<a href="/gestionspromo/affichage_detail_production/?idproduction={row[0]}/"><i class="flaticon-notes icon-wrapper"></i></a>'
                action += f'<a href="/gestionspromo/deleteProduction?idproduction={row[0]}/"><i class="flaticon-delete-can-fill-2 icon-wrapper-delete"></i></a>' 
                tab.append([row[0], formatted_date, row[2], f'Production n° {row[3]}', action])
                #print(row[0], formatted_date , row[2], row[3], action)
                
            except ValueError as ve:
                print(f"Erreur de format de date pour {row[1]}: {ve}")
                formatted_date = str(row[1])  # Utiliser la représentation par défaut en cas d'erreur
                
        result = {
            "draw": int(request.POST.get("draw", 1)),  # Utilisation de POST pour récupérer `draw`
            "recordsTotal": len(production),           # Nombre total d'enregistrements
            "recordsFiltered": len(production),       # Nombre d'enregistrements filtrés (si vous filtrez côté serveur)
            "data": tab
        } 
    except Exception as e: 
        print(f"Erreur lors de la récupération des données : {e}")
        result = {
            "draw": int(request.POST.get("draw", 1)),
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": []
        }  
    return JsonResponse(result) 

def AffichageProduction(request):
    template = loader.get_template('gestionspromo/production.html')
    production = Production(request)
    context = {
        'info': production
    } 
    return HttpResponse(template.render(context,request)) 

    
def getDetailProduction(request):
    rows = []
    try:  
        with connection.cursor() as cursor:
            sql = "select * from articles"
            cursor.execute(sql) 
            
            rows = cursor.fetchall()
            for row in rows:
                print(row)  # Afficher chaque ligne récupérée pour vérification
                
    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")
        
    return rows  # Retourne les données récupérées
    
@csrf_exempt
def deleteProduction(request):
    true = True
    return true
        
@csrf_exempt
def DetailProduction(request):
    try: 
        tab = [] , 
        detail_production = getDetailProduction(request)
        for row in detail_production:
            #print(f'Ato ny maso {row[1]} et {row[2]} et {row[3]} et {row[4]}')           
            action = f'<input type="number" name="action" placeholder=10>'
            tab.append([row[1],row[2],row[3],row[4],action])
            result = { 
                "draw": int(request.POST.get("draw", 1)),  # Utilisation de POST pour récupérer `draw`
                "recordsTotal": len(detail_production),           # Nombre total d'enregistrements
                "recordsFiltered": len(detail_production),       # Nombre d'enregistrements filtrés (si vous filtrez côté serveur)
                "data": tab
            }  
    except Exception as e: 
        print(f"Erreur lors de la récupération des données : {e}")
        result = {
            "draw": int(request.POST.get("draw", 1)),
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": []
        } 
    return JsonResponse(result)    

        
def AffichageDetailProduction(request):
    template = loader.get_template('gestionspromo/detail_production.html')
    detail_production = DetailProduction(request)
    context = {
        'info': detail_production
    }
    return HttpResponse(template.render(context,request))


@csrf_exempt
def insertionProduction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date = data.get('date')
            personnel = data.get('personnel')
            details = data.get('details')

            with connection.cursor() as cursor:
                # Exemple d'insertion de données dans la table atb_prod_index
                sql = "INSERT INTO atb_prod_index (date, pers, number) VALUES (%s, %s, %s)"
                cursor.execute(sql, [date, personnel, details]) 
                connection.commit()  # Valider l'insertion dans la base de données

            return JsonResponse({'success': True, 'message': 'Insertion réussie!'})

        except json.JSONDecodeError:
            # Gestion des erreurs de décodage JSON
            return JsonResponse({'success': False, 'message': 'Erreur de décodage JSON.'}, status=400)
        except Exception as e:
            # Gestion des autres erreurs
            print(f"Erreur lors de l'insertion : {e}")
            return JsonResponse({'success': False, 'message': f'Erreur lors de l\'insertion : {e}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'}, status=405)


@csrf_exempt
def deleteProduction(request):
    if request.method == "GET":
        try:
            # Récupération de l'ID de l'entrée à supprimer depuis la requête GET
            production_id = request.GET.get("idproduction")
            
            # Supprimer le slash à la fin de l'ID si présent
            if production_id.endswith('/'):
                production_id = production_id[:-1]
            
            # Conversion de l'ID en entier
            production_id = int(production_id)
            
            # Exécution de la requête DELETE SQL
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM atb_prod_index WHERE id = %s", [production_id])
            
            # Réponse de succès
            result = {"status": "success", "message": "Production entry deleted successfully."}
            return JsonResponse(result)
        except ValueError as ve: 
            print(f"Erreur de valeur lors de la suppression de l'entrée : {ve}")
            result = {"status": "error", "message": f"Invalid production ID: {str(ve)}"}
            return JsonResponse(result, status=400)  # Statut 400 pour une demande incorrecte
        except Exception as e:
            print(f"Erreur lors de la suppression de l'entrée : {e}")
            result = {"status": "error", "message": f"Error deleting production entry: {str(e)}"}
            return JsonResponse(result, status=500)  # Statut d'erreur 500 pour les erreurs internes du serveur
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)  # Méthode non autorisée