from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
# from .models import PersonnelP


def Login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

@csrf_exempt
def check_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        utilisateur = data.get('utilisateur')
        mdp = data.get('mdp')
          
        # Vérifier si 'utilisateur' ou 'mdp' est null ou vide
        if not utilisateur or not mdp:
            return JsonResponse({'success': False, 'message': 'L\'utilisateur et le mot de passe doivent être fournis.'})
       
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM personnel_p WHERE nummatr = %s AND mdp = %s"
                cursor.execute(sql, [utilisateur, mdp])
                row = cursor.fetchone()
                if row is not None:
                    request.session['nummatr'] = utilisateur
                    # return response
                    return JsonResponse({'success': True, 'message': 'Login successful!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Identifiants incorrects.'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur: {e}'})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})

