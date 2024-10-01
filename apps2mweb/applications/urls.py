from django.urls import path

#Ajouter par Fenosoa
from applications.view.releverprix import ArticleView, Export, RecapRelArticle, RelArtConcurView, RelArtNouveauView,EnseigneView, RelReleveView,ZoneView,IndexReleve


from . import views
from .view import OperationsViews
from .view import LoginViews


#Ajouter par Mialivola
from django.shortcuts import redirect
from django.urls import path
from .view.gestionspromo import Production
from .view.gestionspromo import Recapitulation
from .view.transformationproduit import Transformation
from .view.transformationproduit import DetailTransformation
from .view.personnel import PersonnelGestionViews
from .view.pagerreur import PageError
from django.urls import re_path

#Ajout vaovao Mialivola vaovao bee
from .view.productionTransformation.charcuterie.Production import CharcAffichage


urlpatterns = [
    
    #Redirection vers la page connexion directement
    path('', lambda request: redirect('connexion/', permanent=False)),  # Redirection par défaut vers /connexion/

    path('connexion/', LoginViews.Login, name='connexion'),
    path('check_login/', LoginViews.check_login, name='check_login'),

    path('accueil/', OperationsViews.Accueil, name='accueil'),
    path('gestionspromo/', OperationsViews.Promo, name='gestionspromo'),
    path('rech_operations/', OperationsViews.Rech_Operations, name='rech_operations'),
    path('detail_operations/', OperationsViews.Det_Operations, name='detail_operations'),
    path('Bal_operations/', OperationsViews.Bal_operations, name='Bal_operations'),
    path('personnelRH/', PersonnelGestionViews.ma_vue, {'nom_page': 'personnelRH'}, name='personnelRH'),
    path('detailPersonnel/', PersonnelGestionViews.detailPersonnel, {'nom_page': 'detailPersonnel'}, name='detailPersonnel'),
    path('modifPersonnel/', PersonnelGestionViews.modifPersonnel, {'nom_page': 'modifPersonnel'}, name='modifPersonnel'),
    path('detailPersonnel/conge/', PersonnelGestionViews.conge, {'nom_page': 'conge'}, name='conge'),
    path('detailPersonnel/absence/', PersonnelGestionViews.absence, {'nom_page': 'absence'}, name='absence'),
    path('detailPersonnel/sanction/', PersonnelGestionViews.sanction, {'nom_page': 'sanction'}, name='sanction'),
    path('detailPersonnel/certificatTravail/', PersonnelGestionViews.certificatTravail, {'nom_page': 'certificatTravail'}, name='certificatTravail'),
    path('detailPersonnel/attestationTravail/', PersonnelGestionViews.attestationTravail, {'nom_page': 'attestationTravail'}, name='attestationTravail'),
    path('detailPersonnel/nouveaupers/', PersonnelGestionViews.nouveaupers, {'nom_page': 'nouveaupers'}, name='nouveaupers'),
    path('addpersonnel/', PersonnelGestionViews.addpers, {'nom_page': 'addpers'}, name='addpers'),
    path('updatepersonnel/', PersonnelGestionViews.updatepersonnel, {'nom_page': 'updatepersonnel'}, name='updatepersonnel'),


    path('getListService/', PersonnelGestionViews.getListService, {'nom_page': 'getListService'}, name='getListService'),
    path('getListDepartement/', PersonnelGestionViews.getListDepartement, {'nom_page': 'getListDepartement'}, name='getListDepartement'),

    #Url stg mialivola -> production boulengerie
    path('gestionspromo/production/', Production.Production, name='production'),
    path('gestionspromo/getproduction/', Production.AffichageProduction, name='production'),
    path('gestionspromo/detail_production/', Production.DetailProduction, name='detail_production'),
    path('gestionspromo/affichage_detail_production/', Production.AffichageDetailProduction, name='affichage_detail_production'),
    
    path('gestionspromo/insertionProduction/', Production.insertionProduction, name='insertionProduction'),
    path('gestionspromo/deleteProduction/', Production.deleteProduction, name='deleteProduction'),
    
    #Recapitulation
    path('recapproduction/entree_produit_fini/', Recapitulation.AffichageRecapitulation , name='entree_produit_fini'),
    path('recapproduction/regularisation_produit/', Recapitulation.AffichageRegularisation , name='regularisation_produit'),
    
    path('transformationproduit/transformation/', Transformation.Transformation , name='transformation'),
    path('transformationproduit/recapitulation/', Transformation.Recapitulation , name='recapitulation'),
    
    path('transformationproduit/transformationvaleur/', DetailTransformation.TransformationValeur , name='transformationvaleur'),
     
    # URL après amélioration code 
    path('transformationproduit/charcuterie/', CharcAffichage , name='charcuterie_productions'),   
    path('errorpage/pageerreur/', PageError.PageError , name='pageerreur'),
    
    #--------------------------------FENOSOA--------------------------------------
    #URL Relevé de prix concurrent
    path('releveprix/', IndexReleve.index, name='relevé_prix'),
    #Liste
    path('releveprix/liste-releve/', IndexReleve.liste_releve, name='liste_releve'),
    path('releveprix/liste-enseigne/', EnseigneView.liste_enseigne, name='liste_enseigne'),
    path('releveprix/liste-zone/', ZoneView.liste_zone, name='liste_zone'),
    # path('releveprix/liste-nouveau-article-concurrent/', RelArtNouveauView.liste_rel_art_nouveau, name='liste_rel_art_nouveau'),
    path('releveprix/liste-nomenclature/', ArticleView.applique_filtre_nomenclature, name='applique_filtre_nomenclature'),
    #List ById
    path('releveprix/releve-index/', IndexReleve.select_by_id_releve, name='select_by_id_releve'),
    path('releveprix/liste-detail-releve/', RelReleveView.select_by_id_releve_index, name='select_by_id_releve_index'),
    path('releveprix/liste-rattachement-externe-releve/', RelArtConcurView.select_by_ref_art_concu, name='select_by_ref_art_concu'),
    path('releveprix/liste-historique-releve/', RelReleveView.historique_releve_article, name='historique_releve_article'),
    path('releveprix/info-article/', RelReleveView.select_by_ref_releve_index, name='select_by_ref_releve_index'),
    #Insert
    path('releveprix/ajout-releve/', IndexReleve.ajout_releve, name='ajout_releve'),
    path('releveprix/ajout-enseigne/', EnseigneView.ajout_enseigne, name='ajout_enseigne'),
    path('releveprix/ajout-zone/', ZoneView.ajout_zone, name='ajout_zone'),
    path('releveprix/ajout-rattachement-article-concurrent/', RelArtConcurView.ajout_rattachement_concurrent, name='ajout_rattachement_concurrent'),
    path('releveprix/ajout-article/', ArticleView.ajout_article, name='ajout_article'),
    #import
    path('releveprix/import-releve/', RelReleveView.import_excel_releve, name='import_excel'),
    path('releveprix/import-releve-concurrent/', RelArtConcurView.import_excel_releve_concurrent, name='import_excel_releve_concurrent'),
    path('releveprix/import-rattachement-article-exel/', RelArtConcurView.import_rattachement_concurrent_exel, name='import_rattachement_concurrent_exel'),
    path('releveprix/import-rattachement-concurrent-exel/', RelArtConcurView.import_rattachement_s2m_en_concurrent_exel, name='import_rattachement_s2m_en_concurrent_exel'),
    
    
    #Delete
    path('releveprix/delete-releve/', IndexReleve.delete_releve, name='delete_releve'),
    #Update
    path('releveprix/update-enseigne/<int:id>/', EnseigneView.update_enseigne, name='update_enseigne'),
    path('releveprix/update-zone/<int:id>/', ZoneView.update_zone, name='update_zone'),
    path('releveprix/update-etat-releve/', IndexReleve.update_etat_releve, name='update_etat_releve'),
    path('releveprix/update-information-article-concurrent/', RelReleveView.update_information_article_concurrent, name='update_information_article_concurrent'),
    path('releveprix/validation-etat-releve/', IndexReleve.update_etat_releve_and_index, name='update_etat_releve_and_index'),
    path('releveprix/rattachement-article-s2m/', RelArtConcurView.ajout_rattachement_s2m, name='ajout_rattachement_s2m'),
    #Autre parametre

    path('releveprix/filtre-releve/', IndexReleve.applique_filtre_releve, name='recap_relevé_article'),
    path('releveprix/filtre-article-recapitulatif/', RecapRelArticle.applique_filtre_recap, name='recap_relevé_article'),
    path('releveprix/filtre-article-s2m/', ArticleView.applique_filtre_article_s2m, name='applique_filtre_article_s2m'),
    path('releveprix/filtre-article-concurrent/', RelArtConcurView.filtre_article_concurrent, name='filtre_article_concurrent'),
    # Export
    path('releveprix/pdf-filtre-article-s2m/', Export.generate_pdf_from_filter_s2m, name='generate_pdf_from_filter_s2m'),
    path('releveprix/pdf-filtre-article-concurrent/', Export.generate_pdf_from_filter_concurrent, name='generate_pdf_from_filter_concurrent'),
    path('releveprix/pdf-recap/', Export.generate_pdf_from_recap, name='generate_pdf_from_recap'),
    path('releveprix/pdf-enseigne/', Export.generate_pdf_from_enseigne, name='generate_pdf_from_enseigne'),
    path('releveprix/pdf-zone/', Export.generate_pdf_from_zone, name='generate_pdf_from_zone'),
    path('releveprix/pdf-filtre-releve/', Export.generate_pdf_from_filter_releve, name='generate_pdf_from_filter_releve'),
    path('releveprix/pdf-releve-modal/', Export.generate_pdf_from_releve_modal, name='generate_pdf_from_releve_modal'),
    path('releveprix/pdf-article-rattache/', Export.generate_pdf_from_rattachement_article, name='generate_pdf_from_rattachement_article'),
    # path('releveprix/pdf-detail-releve/', Export.generate_pdf_from_detail_releve, name='generate_pdf_from_detail_releve'),

    
    #--------------------------------FENOSOA--------------------------------------
    

]

# handler404 = 'applications.view.pagerreur.PageError.PageError'
# handler505 = 'applications.view.pagerreur.PageError.custom_server_error'
# Redirection des URLs non définies vers la vue 404

urlpatterns += [
    re_path(r'^.*$', PageError.PageError),
] 