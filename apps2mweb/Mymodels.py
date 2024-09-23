# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class PersonnelP(models.Model):
    id_personnel = models.AutoField(primary_key=True)
    nummatr = models.CharField(unique=True, max_length=10)
    nomcomplet = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    num_tel = models.CharField(max_length=20, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.CharField(max_length=100, blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True)
    date_naiss = models.CharField(max_length=10, blank=True, null=True)
    lieu_naiss = models.CharField(max_length=100, blank=True, null=True)
    date_embauche = models.CharField(max_length=10, blank=True, null=True)
    date_debauche = models.CharField(max_length=10, blank=True, null=True)
    num_cin = models.CharField(max_length=20, blank=True, null=True)
    obtention_cin = models.CharField(max_length=100, blank=True, null=True)
    situ_matri = models.CharField(max_length=15, blank=True, null=True)
    num_ostie = models.CharField(max_length=50, blank=True, null=True)
    num_cnaps = models.CharField(max_length=50, blank=True, null=True)
    titre_prof = models.CharField(max_length=50, blank=True, null=True)
    categorie_prof = models.CharField(max_length=50, blank=True, null=True)
    mdp = models.CharField(max_length=100)
    auth_menu = models.CharField(max_length=255)
    etat = models.IntegerField()
    synchro_att2000 = models.IntegerField(db_comment='0 : pas encore synchroniser; 1 : déjà synchroniser')
    liste_subordonnee = models.TextField(blank=True, null=True)
    depart_lien = models.IntegerField(db_comment='Pour les personnels de grands magasins')
    srvc_gest = models.CharField(max_length=255, blank=True, null=True)
    idfonction = models.IntegerField()
    idmagasin = models.IntegerField()
    etat_notif = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'personnel_p'
