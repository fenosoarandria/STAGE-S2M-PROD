from django.db import models

class PVNRef(models.Model):
    art_pv = models.IntegerField(primary_key=True)
    deb_pv = models.DateField(null=True, blank=True)
    prix_pv = models.FloatField(default=0)
    pvht_pv = models.FloatField(default=0)
    tva_pv = models.FloatField(default=0)

    class Meta:
        db_table = 'pvn_ref'
        unique_together = ('art_pv',)
