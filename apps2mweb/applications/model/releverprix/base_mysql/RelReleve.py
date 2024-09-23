from django.db import models

from applications.model.releverprix.base_mysql.IndexReleve import IndexReleve
from applications.model.releverprix.base_mysql.Zone import Zone

class RelReleve(models.Model):
    id_rel_rel = models.AutoField(primary_key=True)
    num_rel_rel = models.ForeignKey(IndexReleve, on_delete=models.CASCADE, null=True, blank=True, db_column='num_rel_rel')    
    date_rel = models.DateField(null=True, blank=True)
    ref_rel = models.IntegerField(null=True, blank=True)
    libelle_art_rel = models.CharField(max_length=100, null=True, blank=True)
    gencod_rel = models.CharField(max_length=20, null=True, blank=True)
    prix_ref_rel = models.FloatField(null=True, blank=True)
    prix_zone_rel = models.FloatField(null=True, blank=True)
    zone_rel = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True, db_column='zone_rel')        
    lib_zn_rel = models.CharField(max_length=250, null=True, blank=True)
    id_art_conc_rel = models.IntegerField(null=True, blank=True)
    lib_art_concur_rel = models.CharField(max_length=250, null=True, blank=True)
    gc_concur_rel = models.CharField(max_length=20, null=True, blank=True)
    lib_plus_rel = models.CharField(max_length=250, null=True, blank=True)
    prix_concur_rel = models.FloatField(null=True, blank=True)
    etat_rel = models.IntegerField(default=0)
    dt_maj_releve = models.DateTimeField(null=True, blank=True)
    date_val_releve = models.DateTimeField(null=True, blank=True)
    etat_sup_conc = models.IntegerField(default=0)
    statut_rattachement = models.IntegerField(default=0)

    class Meta:
        db_table = 'rel_releve'

