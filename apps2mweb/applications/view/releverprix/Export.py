from datetime import datetime
import pdfkit
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from applications.view.releverprix.ArticleView import applique_filtre_article_s2m
from applications.view.releverprix.EnseigneView import liste_enseigne
from applications.view.releverprix.IndexReleve import applique_filtre_releve, liste_releve
from applications.view.releverprix.RecapRelArticle import applique_filtre_recap
from applications.view.releverprix.RelArtConcurView import filtre_article_concurrent, select_by_ref_art_concu
from applications.view.releverprix.ZoneView import liste_zone
from applications.view.releverprix.helper.date_format import format_date

# ---------------------------------- Front ------------------------------------------------------------------------
def generate_html_content(data, title, headers, row_mapper,date):
    html_content = f'''
    <html>
    <head>
        <style>
            table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
            th, td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}
            th {{ background-color: #f4f4f4; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f1f1f1; }}
            h2 {{ text-align: center; font-size: 18px; color: #333; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h2>{title}{date}</h2>
        <table class="table">
            <thead>
                <tr>
    '''
    for header in headers:
        html_content += f'<th style="color: black; text-align:center; background-color: #7292B2;">{header}</th>'
    
    html_content += '''
                </tr>
            </thead>
            <tbody>
    '''
    
    for row in data:
        html_content += '<tr>'
        for cell in row_mapper(row):
            html_content += f'<td>{cell}</td>'
        html_content += '</tr>'

    html_content += '''
            </tbody>
        </table>
    </body>
    </html>
    '''
    return html_content

# ---------------------------------- Generation en pdf------------------------------------------------------------------------
def generate_pdf(request, filter_func, title, headers, row_mapper, filename):
    if request.method in ['POST', 'GET']:  # Accept both POST and GET methods for simplicity
        try:
            response = filter_func(request)
            data = json.loads(response.content).get('data', [])

            if not data:
                return JsonResponse({'error': 'Aucune donnée trouvée pour la génération du PDF.'}, safe=False)

            html_content = generate_html_content(data, title, headers, row_mapper,datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            pdf = pdfkit.from_string(html_content, False, configuration=settings.PDFKIT_CONFIG)

            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {e}")
            return JsonResponse({'error': 'Erreur lors de la génération du PDF.'}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)





# ----------------------------------------------------------------------------------------------------------
@csrf_exempt
def generate_pdf_from_filter_s2m(request):
    def row_mapper(row):
        return [
            row.get("art", ""),
            row.get("lib", ""),
            row.get("ray", ""),
            row.get("gencod", ""),
            f"{row.get('sec', '')} - {row.get('ray', '')} - {row.get('fam', '')} - {row.get('sfam', '')}",
            f"{row.get('fn', '')} - {row.get('raison_social_frs', '')}",
            row.get("tva_vte", ""),
            format_date(row.get("date_creat", "")),
            format_date(row.get("date_maj", "")),
            row.get("article_rattache", 0)
        ]
    
    return generate_pdf(request, applique_filtre_article_s2m, 'Rapport des Articles S2M le ', 
                        ['Action', 'Libelle', 'Rayon', 'Gencode', 'Description', 'Fournisseur', 'TVA Vente', 'Date Creation', 'Date Maj', 'Article Rattache'],
                        row_mapper, 'S2m.pdf')

@csrf_exempt
def generate_pdf_from_filter_concurrent(request):
    def row_mapper(row):
        return [
            row.get("libelle_ens", ""),
            row.get("ref_rel", ""),
            row.get("lib_art_concur_rel", ""),
            row.get("gc_concur_rel", ""),
            row.get("prix_concur_rel", "")
        ]
    
    return generate_pdf(request, filtre_article_concurrent, 'Rapport des Articles Concurrent le ', 
                        ['Enseigne','Reference', 'Libelle article','Gencode', 'Prix'],
                        row_mapper, 'Concurrent.pdf')

@csrf_exempt
def generate_pdf_from_recap(request):
    def row_mapper(row):
        prixRefRel = f"{row.get('prix_ref_rel', 'N/A'):,}" if row.get('prix_ref_rel') is not None else 'N/A'
        prixConcurRel = f"{row.get('prix_concur_rel', 'N/A'):,}" if row.get('prix_concur_rel') is not None else 'N/A'
        differencePrix = (row.get('prix_ref_rel') - row.get('prix_concur_rel')) if row.get('prix_ref_rel') is not None and row.get('prix_concur_rel') is not None else 'N/A'
        return [
            row.get('date_rel', ''),
            row.get('num_rel_rel', ''),
            row.get('libelle_ens', ''),
            row.get('ref_rel', ''),
            row.get('libelle_art_rel', ''),
            row.get('gencod_rel', ''),
            row.get('article_data', {}).get('ray', ''),
            prixRefRel,
            row.get('id_art_conc_rel', ''),
            row.get('gc_concur_rel', ''),
            row.get('lib_art_concur_rel', ''),
            prixConcurRel,
            differencePrix
        ]
    
    return generate_pdf(request, applique_filtre_recap, 'Rapport des Recapitulation le ', 
                        ['DATE', 'RELEVE', 'ENSEIGNE', 'REF', 'LIBELLE', 'GENECODE', 'RAY', 'PRIX', 'REF CONCURRENTS', 'GENECODE CONCURRENTS', 'LIBELLE CONCURRENTS', 'PRIX CONCURRENTS', 'ECART'],
                        row_mapper, 'rapport_recapitulatif.pdf')

@csrf_exempt
def generate_pdf_from_enseigne(request):
    def row_mapper(row):
        return [
            row.get("enseigne_ens", ""),
            row.get("libelle_ens", ""),
            row.get("lib_plus_ens", "")
        ]
    
    return generate_pdf(request, liste_enseigne, 'Rapport des Enseignes le ', 
                        ['Numero enseigne', 'Libelle enseigne', 'Autres rubrique'],
                        row_mapper, 'rapport_enseigne.pdf')

@csrf_exempt
def generate_pdf_from_zone(request):
    
    def row_mapper(row):
        return [
            row.get("zone_zn", ""),
            row.get("libelle_zn", ""),
            row.get("lib_plus_zn", "")
        ]
    
    return generate_pdf(request, liste_zone, 'Rapport des Zones le ', 
                        ['Numero zone', 'Libelle', 'Autre rubrique'],
                        row_mapper, 'rapport_zone.pdf')

@csrf_exempt
def generate_pdf_from_filter_releve(request):
    if request.method == 'POST':
        try:

            def row_mapper(row):
                return [
                    row.get("id_releve", ""),
                    row.get("libelle_ens", ""),
                    row.get("libelle_zn", ""),
                    row.get("libelle_releve", ""),
                    row.get("date_releve", ""),
                    row.get("lib_plus_releve", ""),
                    row.get("dt_maj_releve", ""),
                    row.get("nb_article", ""),
                    row.get('lib_etat_rel', '')
                ]
            
            return generate_pdf(request, applique_filtre_releve, f'Rapport des releves le ', 
                                ['Numero releve', 'Concurent', 'Zone releve', 'Nom releve', 'Date creation', 'Autre info', 'Date maj', 'Nombre article', 'Etat'],
                                row_mapper, 'rapport_releve.pdf')
        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {e}")
            return JsonResponse({'error': 'Erreur lors de la génération du PDF.'}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)

@csrf_exempt
def generate_pdf_from_releve_modal(request):
    
    def row_mapper(row):
        return [
            row.get("id_releve", ""),
                row.get("libelle_releve", ""),
                row.get("libelle_ens", ""),
                row.get("date_releve", "")
        ]
    return generate_pdf(request, liste_releve, f'Rapport des releves le ', 
                            ['Numero releve', 'Libelle', 'Enseigne', 'Date creation'],
                            row_mapper, 'rapport_releve_modal.pdf')

@csrf_exempt
def generate_pdf_from_rattachement_article(request):
    if request.method == 'POST':
        try:

            def row_mapper(row):
                return [
                    row.get("id_art_concur", ""),
                    row.get("libelle_ens", ""),
                    row.get("ref_ac", ""),
                    row.get("libelle_ac", ""),
                    row.get("gencod_ac", "")
                ]
            return generate_pdf(request, select_by_ref_art_concu, f'Rapport des articles rattacher le ', 
                                ['Id', 'Enseigne', 'Reference', 'Libelle', 'Gencode'],
                                row_mapper, 'rapport_rattachement_article.pdf')
        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {e}")
            return JsonResponse({'error': 'Erreur lors de la génération du PDF.'}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)
