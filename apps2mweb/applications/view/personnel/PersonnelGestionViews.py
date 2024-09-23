import json
import os
from io import BytesIO

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.db import connection
from django.utils import timezone
from datetime import datetime
from ...forms import UploadImageForm
from django.conf import settings

from django.template.loader import render_to_string, get_template
from xhtml2pdf import pisa

from django.views.decorators.csrf import csrf_exempt
from apps2mweb.settings import STATICFILES_DIRS
from django.template.loader import get_template
import pdfkit

def ma_vue(request, nom_page):
    if nom_page == 'personnelRH':
    	with connection.cursor() as cursor:
	    	cursor.execute("SELECT p.*,m.Num_magasin,m.Nom_magasin, fp.nom_fonction FROM personnel_p p join magasin m on m.id_magasin = p.idmagasin join fonction_p fp on fp.id_fonction = p.idfonction WHERE p.etat = 1")
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

    	return render(request, 'personnel/personnelRH.html', context) 


def nouveaupers(request, nom_page):
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM categorie")		
		listcategorie = cursor.fetchall()
		cursor.execute("SELECT * FROM direction")		
		listdirection = cursor.fetchall()
		cursor.execute("SELECT * FROM fonction_p order by nom_fonction asc")		
		listfonction = cursor.fetchall()

	return render(request, 'personnel/nouveauPersonnel.html',  {'listcategorie':listcategorie, 'listdirection':listdirection, 'listfonction':listfonction})

def detailPersonnel(request, nom_page):
	matricule = request.POST.get('matricule')
	with connection.cursor() as cursor:
		cursor.execute("SELECT personnel_p.*,fonction_p.*,magasin.Nom_magasin FROM personnel_p join fonction_p on fonction_p.id_fonction = personnel_p.idfonction join magasin on magasin.id_magasin = personnel_p.idmagasin where nummatr =  %s", (matricule,))
		infopers = cursor.fetchone()
		query = "SELECT * FROM personnel_p WHERE idfonction IN (%s) AND idmagasin = %s"
		parametres = (infopers[24], infopers[28])
		dateemb = datetime.strptime(infopers[11], '%d-%m-%Y')
		dateemb = dateemb.strftime('%Y-%m-%d')
		now = datetime.now().strftime('%Y-%m-%d')
		cursor.execute(query, parametres)
		listsub = cursor.fetchall()

		cursor.execute("SELECT * from enfant_p where idpersonnel_enf =  %s", (infopers[0],))
		enfant = cursor.fetchall()
		updated_enfs = []
		for enf in enfant:
			date_naissance = datetime.strptime(enf[3], '%d-%m-%Y')
			date_actuelle = datetime.now()
			age = date_actuelle.year - date_naissance.year - ((date_actuelle.month, date_actuelle.day) < (date_naissance.month, date_naissance.day))
			updated_enf = list(enf)
			updated_enf[4] = age
			updated_enfs.append(updated_enf)
		# print(infopers[0])
	with connection.cursor() as cursor:
	    	cursor.execute("SELECT * FROM `historique_p` join personnel_p on personnel_p.id_personnel = historique_p.idpersonnel join magasin on magasin.id_magasin = historique_p.idmag_actu where historique_p.idpersonnel =  %s", (infopers[0],))
	    	rows = cursor.fetchall()
	    	updated_rows = []
	    	for row in rows:
	    		# print(row)
	    		if row[4] == 0:
	    			print('ato')
	    			cursor.execute("SELECT * FROM magasin WHERE id_magasin =  1")
	    			testmagancien = cursor.fetchone()
		    		updated_row = list(row)
		    		updated_row[4] = testmagancien[2]
		    	else:
	    			# print(row[4])
		    		cursor.execute("SELECT * FROM magasin WHERE id_magasin =  %s", (row[4],))
	    			testmagancien = cursor.fetchone()
		    		updated_row = list(row)
		    		updated_row[4] = testmagancien[2]
		    		# updated_rows.append(updated_row)

		    		# print(row[5])

		    	if row[5] == '0':
		    		print('io')
		    		cursor.execute("SELECT * FROM magasin WHERE id_magasin =  1")
	    			test = cursor.fetchone()
		    		updated_row = list(row)
		    		updated_row[5] = test[2]
		    		# updated_rows.append(updated_row)
		    	else:
		    		cursor.execute("SELECT * FROM magasin WHERE id_magasin =  %s", (row[5],))
	    			test = cursor.fetchone()
		    		updated_row = list(row)
		    		updated_row[5] = test[2]
		    		# updated_rows.append(updated_row)
		    		# histo = {'rows': updated_rows}
		    	updated_rows.append(updated_row)
		    	# cursor.execute("SELECT * FROM personnel_p join fonction_p on fonction_p.id_fonction = personnel_p.idfonction where nummatr =  %s", (matricule,))
		    	# infopers = cursor.fetchone()
		    	print(updated_rows)



	return render(request, 'personnel/detailPersonnel.html', {'rows': updated_rows, 'infopers': infopers, 'enfant':updated_enfs, 'listsub':listsub, 'dateemb': dateemb, 'now':now})

def modifPersonnel(request, nom_page):
	matricule = request.POST.get('matricule')
	with connection.cursor() as cursor:
		cursor.execute("SELECT personnel_p.*,fonction_p.*,magasin.Nom_magasin, direction.*, departement.* FROM personnel_p join fonction_p on fonction_p.id_fonction = personnel_p.idfonction join magasin on magasin.id_magasin = personnel_p.idmagasin LEFT JOIN direction ON direction.id = personnel_p.id_dir LEFT JOIN departement ON departement.id = personnel_p.id_dep where nummatr =  %s", (matricule,))
		infopers = cursor.fetchone()
		print(infopers)
		dateemb = datetime.strptime(infopers[11], '%d-%m-%Y')
		dateemb = dateemb.strftime('%Y-%m-%d')
		now = datetime.now().strftime('%Y-%m-%d')
		options = ["H.C", "OS1", "OS2", "OS3", "1A", "2A", "3A", "4A", "5A", "1B", "2B", "3B", "4B", "5B", "OP1", "OP2", "OP3"]
		cursor.execute("SELECT * FROM categorie")		
		listcategorie = cursor.fetchall()
		cursor.execute("SELECT * FROM direction")		
		listdirection = cursor.fetchall()
		cursor.execute("SELECT * from enfant_p where idpersonnel_enf =  %s", (infopers[0],))
		enfant = cursor.fetchall()
		cursor.execute("SELECT * FROM service")
		service = cursor.fetchall()
		cursor.execute("SELECT * FROM departement")
		departements = cursor.fetchall()
		cursor.execute("SELECT * FROM fonction_p order by nom_fonction asc")		
		fonctions = cursor.fetchall()
		updated_enfs = []
		for enf in enfant:
			date_naissance = datetime.strptime(enf[3], '%d-%m-%Y')
			date_actuelle = datetime.now()
			age = date_actuelle.year - date_naissance.year - ((date_actuelle.month, date_actuelle.day) < (date_naissance.month, date_naissance.day))
			updated_enf = list(enf)
			updated_enf[4] = age
			updated_enfs.append(updated_enf)
	return render(request, 'personnel/modifPersonnel.html', {'infopers': infopers, 'enfant':updated_enfs,  'dateemb': dateemb, 'now':now,  'options':options, 'listcategorie':listcategorie, 'listdirection':listdirection, 'service':service, 'departements':departements, 'fonctions': fonctions}) 


def conge(request, nom_page):
	print(request.GET.get('attribut'))
	with connection.cursor() as cursor:
		cursor.execute("SELECT nummatr,nomcomplet,prenom,categorie_prof, nom_fonction,id_personnel FROM personnel_p join fonction_p on  fonction_p.id_fonction = personnel_p.idfonction WHERE nummatr =  %s", (request.GET.get('attribut'),))
		infopers = cursor.fetchone()
		cursor.execute("SELECT * FROM conge_p JOIN personnel_p ON personnel_p.id_personnel = conge_p.idpersonnel WHERE conge_p.idpersonnel = %s ORDER BY conge_p.id_conge DESC", (infopers[5],))		
		listconge = cursor.fetchall()

	return render(request, 'personnel/conge.html',  {'infopers': infopers, 'listconge':listconge})


def absence(request, nom_page):
	print(request.GET.get('attribut'))
	with connection.cursor() as cursor:
		cursor.execute("SELECT nummatr,nomcomplet,prenom,categorie_prof, nom_fonction,id_personnel FROM personnel_p join fonction_p on  fonction_p.id_fonction = personnel_p.idfonction WHERE nummatr =  %s", (request.GET.get('attribut'),))
		infopers = cursor.fetchone()
		cursor.execute("select * from absence_p join personnel_p on personnel_p.id_personnel = absence_p.idpersonnel join magasin on magasin.id_magasin = personnel_p.idmagasin where absence_p.idpersonnel = %s order by id_absence desc", (infopers[5],))		
		listconge = cursor.fetchall()

	return render(request, 'personnel/absence.html',  {'infopers': infopers, 'listconge':listconge})

def sanction(request, nom_page):
	print(request.GET.get('attribut'))
	with connection.cursor() as cursor:
		cursor.execute("SELECT nummatr,nomcomplet,prenom,categorie_prof, nom_fonction,id_personnel FROM personnel_p join fonction_p on  fonction_p.id_fonction = personnel_p.idfonction WHERE nummatr =  %s", (request.GET.get('attribut'),))
		infopers = cursor.fetchone()
		cursor.execute("select * from sanctionpers join personnel_p on personnel_p.id_personnel = sanctionpers.idpersonnel where sanctionpers.idpersonnel = %s order by id_sanction desc", (infopers[5],))		
		listconge = cursor.fetchall()

	return render(request, 'personnel/sanction.html',  {'infopers': infopers, 'listconge':listconge})

@csrf_exempt
def certificatTravail(request, nom_page):
	with connection.cursor() as cursor:
		cursor.execute("SELECT nummatr,nomcomplet,prenom,categorie_prof, nom_fonction FROM personnel_p join fonction_p on  fonction_p.id_fonction = personnel_p.idfonction WHERE nummatr =  %s", (request.POST['matricule'],))
		inforpers = cursor.fetchone()
		maintenant = datetime.now()
		maintenant = maintenant.date()
		datedeb = request.POST['db'].split("-")
		datefn = request.POST['fn'].split("-")
		maintenant = request.POST['fn'].split("-")
		mois = {
		    "01": "janvier",
		    "02": "février",
		    "03": "mars",
		    "04": "avril",
		    "05": "mai",
		    "06": "juin",
		    "07": "juillet",
		    "08": "août",
		    "09": "septembre",
		    "10": "octobre",
		    "11": "novembre",
		    "12": "décembre"
		}
		datedeb = str(datedeb[2]) + " " + str(mois[datedeb[1]]) + " " +  str(datedeb[0])
		datefn = str(datefn[2]) + " " + str(mois[datefn[1]]) + " " +  str(datefn[0])
		maintenant = str(maintenant[2]) + " " + str(mois[maintenant[1]]) + " " +  str(maintenant[0])
		context = {	
	 	       'datedeb':datedeb,
	 	       'datefn':datefn,
	 	       'maintenant':maintenant,
	 	       'asset': STATICFILES_DIRS[0],
	 	       'matricule' : request.POST['matricule'],
	 	       'personnel' : inforpers,
	 	}
		template = get_template("certificat.html")
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = f'filename={request.POST["matricule"]}_certificat.pdf'

		html = template.render(context)
		pdf = BytesIO()
		pisa.pisaDocument(BytesIO(html.encode("utf-8")), pdf)
		doc_dir = os.path.join(STATICFILES_DIRS[0], 'doc')
		lien = "/static/doc/"+request.POST["matricule"]+"_certificat.pdf";
		lien = "/static/doc/" + str(request.POST["matricule"]) + "_certificat.pdf"
		print(lien)
		if not os.path.exists(doc_dir):
			os.makedirs(doc_dir)
		output_pdf_path = os.path.join(doc_dir, str(request.POST["matricule"]) + '_certificat.pdf')
		res = HttpResponse(pdf.getvalue(), content_type="application/pdf")
		pdf.seek(0)
		with open(output_pdf_path, 'wb') as f:
			f.write(pdf.read())

		return JsonResponse({'nom':lien})


@csrf_exempt
def attestationTravail(request, nom_page):
	with connection.cursor() as cursor:
		cursor.execute("SELECT nummatr,nomcomplet,prenom,categorie_prof, nom_fonction FROM personnel_p join fonction_p on  fonction_p.id_fonction = personnel_p.idfonction WHERE nummatr =  %s", (request.POST['matricule'],))
		inforpers = cursor.fetchone()
		maintenant = datetime.now()
		maintenant = maintenant.date()
		datedeb = request.POST['db'].split("-")
		maintenant = str(maintenant).split("-")
		mois = {
		    "01": "janvier",
		    "02": "février",
		    "03": "mars",
		    "04": "avril",
		    "05": "mai",
		    "06": "juin",
		    "07": "juillet",
		    "08": "août",
		    "09": "septembre",
		    "10": "octobre",
		    "11": "novembre",
		    "12": "décembre"
		}
		datedeb = str(datedeb[2]) + " " + str(mois[datedeb[1]]) + " " +  str(datedeb[0])
		# datefn = str(datefn[2]) + " " + str(mois[datefn[1]]) + " " +  str(datefn[0])
		maintenant = str(maintenant[2]) + " " + str(mois[maintenant[1]]) + " " +  str(maintenant[0])
		context = {	
	 	       'datedeb':datedeb,
	 	       'maintenant':maintenant,
	 	       'asset': STATICFILES_DIRS[0],
	 	       'matricule' : request.POST['matricule'],
	 	       'personnel' : inforpers,
	 	}
		template = get_template("attestation.html")
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = f'filename={request.POST["matricule"]}_certificat.pdf'

		html = template.render(context)
		pdf = BytesIO()
		pisa.pisaDocument(BytesIO(html.encode("utf-8")), pdf)
		doc_dir = os.path.join(STATICFILES_DIRS[0], 'doc')
		lien = "/static/doc/"+request.POST["matricule"]+"_certificat.pdf";
		lien = "/static/doc/" + str(request.POST["matricule"]) + "_certificat.pdf"
		print(lien)
		if not os.path.exists(doc_dir):
			os.makedirs(doc_dir)
		output_pdf_path = os.path.join(doc_dir, str(request.POST["matricule"]) + '_certificat.pdf')
		res = HttpResponse(pdf.getvalue(), content_type="application/pdf")
		pdf.seek(0)
		with open(output_pdf_path, 'wb') as f:
			f.write(pdf.read())
			
		return JsonResponse({'nom':lien})
		
@csrf_exempt
def addpers(request, nom_page):
	if request.method == 'POST':
		# print(request.POST)
		with connection.cursor() as cursor:
			sqlinsert = 'INSERT INTO `personnel_p` (`nummatr`, `nomcomplet`, `prenom`, `num_tel`, `mail`, `ville`, `adresse`, `sexe`, `date_naiss`, `lieu_naiss`, `date_embauche`,'
			sqlinsert += '`date_debauche`, `num_cin`, `obtention_cin`, `situ_matri`, `num_ostie`, `num_cnaps`, `titre_prof`, `categorie_prof`, `mdp`, `auth_menu`,'
			sqlinsert += '`etat`, `synchro_att2000`, `liste_subordonnee`, `depart_lien`, `srvc_gest`, `idfonction`, `idmagasin`, `etat_notif`, `id_dep`, `id_srv`, `is_lead_dep`, `is_lead_srv`,'
			sqlinsert += '`is_lead_dir`, `id_dir`)'
			sqlinsert += ' VALUES ("'+str(request.POST["matricule"])+'","'+str(request.POST["nom"])+'","'+str(request.POST["prenom"])+'" ,"'+str(request.POST["txt_phonePersonnel"])+'"'
			sqlinsert += ',"'+str(request.POST["txt_mailProf"])+'" ,"'+str(request.POST["residence"])+'" ,"'+str(request.POST["adresse"])+'"'
			sqlinsert += ',"'+str(request.POST["sexe"])+'" ,"'+str(request.POST["datenaiss"])+'" ,"'+str(request.POST["lieunaiss"])+'"'
			sqlinsert += ',"'+str(request.POST["date_embauche"])+'" ,NULL ,"'+str(request.POST["cin"])+'" '
			sqlinsert += ',"'+str(request.POST["date_cin"])+'" , "'+str(request.POST["situationmaritale"])+'" ,"'+str(request.POST["ostie"])+'" '
			sqlinsert += ',"'+str(request.POST["cnaps"])+'" , "'+str(request.POST["contrat"])+'" ,"'+str(request.POST["categorie"])+'" '
			sqlinsert += ',"s2mweb" , "", 1, 1, NULL, 0, NULL, '+str(request.POST["fonction"])+', '+str(request.POST["lieutravail"])+''
			sqlinsert += ',0 , '+str(request.POST["departement"])+', '+str(request.POST["service"])+', '+str(request.POST["lead_dep"])+''
			sqlinsert += ',0 , '+str(request.POST["lead_srv"])+', '+str(request.POST["lead_dir"])+')' 
			
			form = UploadImageForm(request.POST, request.FILES)

			uploaded_file = request.FILES['photoDuPersonnel']
			file_name = uploaded_file.name
			upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
			file_path = os.path.join(upload_dir, file_name)
			# Si le fichier existe déjà, renommez-le
			if os.path.exists(file_path):
				base, extension = os.path.splitext(file_name)
				counter = 1
				new_file_name = f"{base}_{counter}{extension}"
				new_file_path = os.path.join(upload_dir, new_file_name)
				while os.path.exists(new_file_path):
					counter += 1
					new_file_name = f"{base}_{counter}{extension}"
					new_file_path = os.path.join(upload_dir, new_file_name)
					file_name = new_file_name

			# Enregistrez le fichier
			with open(os.path.join(upload_dir, file_name), 'wb+') as destination:
				for chunk in uploaded_file.chunks():
					destination.write(chunk)
					# cursor.execute(sqlinsert)
		return JsonResponse({'status': 'success'})

		
@csrf_exempt
def updatepersonnel(request, nom_page):
	if request.method == 'POST':
		print(request.POST)
		with connection.cursor() as cursor:
			# print(sqlupdate)
			# sqlupdate = 'UPDATE `personnel_p` SET `nummatr` = "'+str(request.POST["matricule"])+'", `nomcomplet` = "'+str(request.POST["nom"])+'", `prenom` = "'+str(request.POST["prenom"])+'" ,`num_tel` = "'+str(request.POST["txt_phonePersonnel"])+'", `mail` = "'+str(request.POST["txt_mailProf"])+'", `ville` = "'+str(request.POST["residence"])+'", `adresse` = "'+str(request.POST["adresse"])+'", `sexe` = "'+str(request.POST["sexe"])+'", `date_naiss`="'+str(request.POST["datenaiss"])+'", `lieu_naiss`="'+str(request.POST["lieunaiss"])+'",`date_embauche`="'+str(request.POST["date_embauche"])+'",`date_debauche`=NULL, `num_cin`="'+str(request.POST["cin"])+'" , `obtention_cin`="'+str(request.POST["date_cin"])+'",`situ_matri`="'+str(request.POST["situationmaritale"])+'", `num_ostie`="'+str(request.POST["ostie"])+'", `num_cnaps`="'+str(request.POST["cnaps"])+'", `titre_prof`="'+str(request.POST["contrat"])+'", `categorie_prof`="'+str(request.POST["categorie"])+'", `mdp`="s2mweb", `auth_menu`="",`etat`=1, `synchro_att2000`=1, `liste_subordonnee`=NULL, `depart_lien`=0, `srvc_gest`=NULL, `idfonction`='+str(request.POST["fonction"])+', `idmagasin`= '+str(request.POST["lieutravail"])+', `etat_notif`=0, `id_dep`='+str(request.POST["departement"])+', `id_srv`='+str(request.POST["service"])+', `is_lead_dep`='+str(request.POST["lead_dep"])+', `is_lead_srv`= '+str(request.POST["lead_srv"])+' `is_lead_dir`='+str(request.POST["lead_dir"])+', `id_dir`'+str(request.POST["direction"])+''
			form = UploadImageForm(request.POST, request.FILES)
			uploaded_file = request.FILES['photoDuPersonnel']
			file_name = uploaded_file.name
			upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
			file_path = os.path.join(upload_dir, file_name)
			# Si le fichier existe déjà, renommez-le
			if os.path.exists(file_path):
				base, extension = os.path.splitext(file_name)
				counter = 1
				new_file_name = f"{base}_{counter}{extension}"
				new_file_path = os.path.join(upload_dir, new_file_name)
				while os.path.exists(new_file_path):
					counter += 1
					new_file_name = f"{base}_{counter}{extension}"
					new_file_path = os.path.join(upload_dir, new_file_name)
					file_name = new_file_name

			# Enregistrez le fichier
			with open(os.path.join(upload_dir, file_name), 'wb+') as destination:
				for chunk in uploaded_file.chunks():
					destination.write(chunk)
					# cursor.execute(sqlupdate)
		return JsonResponse({'status': 'success'})

@csrf_exempt
def getListService(request, nom_page):
	if request.method == 'POST':
		print(request.POST['id'])
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM service  where id_direction =  %s", (request.POST['id'],))
			inforpers = cursor.fetchall()
		html = ''
		html += '<label for="" style="font-size: 0.8em;;">SERVICE : </label><input type="hidden" name="lead_srv" value="0"><input class="check_sexe" id="lead_srv" name="lead_srv" type="checkbox" value="1">'
		html += '<select name="service" id="service" onchange="getservice(this.value)" class="form-control">'
		html += '<option value="" disabled="" selected="">-- Sélectionnez une service --</option>'
		print(inforpers)
		for row in inforpers:
			html += '<option value="' + str(row[0]) + '">' + row[1] + '</option>'

		html += '</select>'
		return JsonResponse({'html':html})

@csrf_exempt
def getListDepartement(request, nom_page):
	if request.method == 'POST':
		print(request.POST['id'])
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM departement  where id_serv =  %s", (request.POST['id'],))
			inforpers = cursor.fetchall()
		html = ''
		html += '<label for="" style="font-size: 0.8em;;">DEPARTEMENT : </label><input type="hidden" name="lead_dep" value="0"><input class="check_dep" id="lead_dep" name="lead_dep" type="checkbox" value="1">'
		html += '<select name="departement" id="departement" onchange="getFonction(this.value)" class="form-control selectpicker">'
		html += '<option value="" disabled="" selected="">-- Sélectionnez une département --</option>'
		for row in inforpers:
			html += '<option value="' + str(row[0]) + '">' + row[1] + '</option>'

		html += '</select>'
		return JsonResponse({'html':html})

