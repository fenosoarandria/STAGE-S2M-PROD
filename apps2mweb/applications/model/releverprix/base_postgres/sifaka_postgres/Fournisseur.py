from django.db import models

class Fournisseur(models.Model):
    id_frs = models.IntegerField(primary_key=True)
    raison_social_frs = models.CharField(max_length=250)
    nif_frs = models.CharField(max_length=250)
    stat_frs = models.CharField(max_length=250)
    rcs_frs = models.CharField(max_length=250)
    adresse_frs = models.CharField(max_length=250)
    contact_frs = models.CharField(max_length=250)
    mail_frs = models.CharField(max_length=250)
    id_type_frs = models.IntegerField()
    numero_frs = models.IntegerField()
    lib_type_frs = models.CharField(max_length=250)

    class Meta:
        db_table = 'fournisseur'
        unique_together = (('id_frs',),)  # Contrainte unique pour la colonne `id_frs`
