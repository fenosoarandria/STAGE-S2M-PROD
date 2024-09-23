from django.db import models

from applications.model.releverprix.base_mysql.Enseigne import Enseigne
from applications.model.releverprix.base_mysql.Zone import Zone

class RelArtNouveau(models.Model):
    id_nouv = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    prix = models.FloatField(blank=True, null=True)
    gencode = models.CharField(max_length=50, blank=True, null=True)
    id_enseigne = models.ForeignKey(Enseigne, on_delete=models.CASCADE, null=True, blank=True, db_column='id_enseigne')
    id_zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True, db_column='id_zone')    
    libelle_plus = models.TextField(blank=True, null=True)
    image_art = models.CharField(max_length=255, blank=True, null=True)
    date_maj = models.DateTimeField(blank=True, null=True)
    date_trans = models.DateTimeField(blank=True, null=True)
    etat = models.IntegerField(default=0)

    class Meta:
        db_table = 'rel_art_nouveau'
        
