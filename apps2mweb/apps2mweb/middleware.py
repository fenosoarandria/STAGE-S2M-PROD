# votre_application/middleware.py
from django.shortcuts import redirect

class CheckCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifiez si le cookie "id_personnel" existe
        # if 'id_personnel' not in request.COOKIES and request.path != '/connexion/':
        #     # Redirigez vers la page de connexion si le cookie est absent
        #     print("Cookie 'id_personnel' non trouvé. Redirection vers la page de connexion.")
        #     return redirect('http://127.0.0.1:8000/connexion/')
        # else :
        #     print("Il y a peut être un problème.")
        response = self.get_response(request)
        return response
