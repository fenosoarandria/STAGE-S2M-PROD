from django.db import models

from applications.model.releverprix.base_mysql.Zone import Zone
from applications.model.releverprix.base_mysql.Enseigne import Enseigne

class IndexReleve(models.Model):
    id_releve = models.AutoField(primary_key=True)
    enseigne_releve = models.ForeignKey(Enseigne, on_delete=models.CASCADE, null=True, blank=True, db_column='enseigne_releve')
    zone_releve = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True, db_column='zone_releve')
    libelle_releve = models.CharField(max_length=250, null=True, blank=True)
    date_releve = models.DateField(null=True, blank=True)
    lib_plus_releve = models.CharField(max_length=250, null=True, blank=True)
    dt_maj_releve = models.DateTimeField(null=True, blank=True)
    dt_trans_releve = models.DateTimeField(null=True, blank=True)
    etat_rel = models.IntegerField()    

    class Meta:
        db_table = 'rel_index_releve'
