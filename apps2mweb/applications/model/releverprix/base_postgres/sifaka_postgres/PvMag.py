from django.db import models

class PvMag(models.Model):
    id_pv = models.BigAutoField(primary_key=True)
    mag_pv = models.CharField(max_length=3, blank=True, null=True)
    art_pv = models.IntegerField(blank=True, null=True)
    deb_pv = models.IntegerField(blank=True, null=True)
    pvnttc_pv = models.FloatField(blank=True, null=True)
    maj_pv = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'pvmag'
        unique_together = (('mag_pv', 'art_pv'),)
        managed = True  # Indique que Django gère cette table
