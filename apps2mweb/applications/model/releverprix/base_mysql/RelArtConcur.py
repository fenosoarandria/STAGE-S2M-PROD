from django.db import models

class RelArtConcur(models.Model):
    id_art_concur = models.AutoField(primary_key=True)
    enseigne_ac = models.IntegerField(null=True, blank=True)
    ref_ac = models.IntegerField(null=True, blank=True)
    libelle_ac = models.CharField(max_length=60, null=True, blank=True)
    gencod_ac = models.CharField(max_length=20, null=True, blank=True)
    etat = models.IntegerField(default=1)
    date_maj = models.DateTimeField(null=True, blank=True)
    user_maj = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'rel_art_concur'
        
