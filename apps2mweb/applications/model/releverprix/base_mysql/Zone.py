from django.db import models

class Zone(models.Model):
    zone_zn = models.AutoField(primary_key=True)
    libelle_zn = models.CharField(max_length=250, null=True, blank=True)
    lib_plus_zn = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'rel_zone_prix'
