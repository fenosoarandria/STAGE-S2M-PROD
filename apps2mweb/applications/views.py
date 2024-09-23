from django.shortcuts import render
from django.db import connection
from django.utils import timezone
from datetime import datetime

def ma_vue(request, nom_page):
    if nom_page == 'personnelRH':
    	with connection.cursor() as cursor:
	    	cursor.execute("SELECT p.*,m.Num_magasin,m.Nom_magasin, fp.nom_fonction FROM personnel_p p join magasin m on m.id_magasin = p.idmagasin join fonction_p fp on fp.id_fonction = p.idfonction LIMIT 500")
	    	rows = cursor.fetchall()
	    	today = timezone.now().date()
	    	updated_rows = []
	    	for row in rows:
	    		if row[11]:
	    			date_str = row[11]
	    			try:
			    		date_str = row[11]
			    		date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
			    		difference = today - date_obj
			    		years = difference.days // 365
			    		months = (difference.days % 365) // 30
			    		days = (difference.days % 365) % 30
			    		difference_formatted = f"{years} années, {months} mois et {days} jours"
			    		updated_row = list(row)
			    		updated_row[11] = difference_formatted
			    		updated_rows.append(updated_row)
			    		# print(updated_rows)
			    	except ValueError:
			    		print(f"La date '{date_str}' n'est pas dans le bon format. Ignorée.")
			    	else:
			    		# print("La valeur de la colonne 11 est nulle ou vide.")
			    		context = {'rows': updated_rows}

    	return render(request, 'personnelRH.html', context) 