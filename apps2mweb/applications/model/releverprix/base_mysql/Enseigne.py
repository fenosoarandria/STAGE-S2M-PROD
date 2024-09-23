from django.db import models

class Enseigne(models.Model):
    enseigne_ens = models.AutoField(primary_key=True)
    libelle_ens = models.CharField(max_length=250, null=True, blank=True)
    lib_plus_ens = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'rel_enseigne'

    