from django.db import models

class Article(models.Model):
    id_art = models.AutoField(primary_key=True)  # Utilise une séquence par défaut pour l'auto-incrémentation
    art = models.IntegerField(unique=True)  # Clé unique
    lib = models.CharField(max_length=50)
    gencod = models.CharField(max_length=15)
    fn = models.IntegerField(null=True, blank=True)
    lib_caisse = models.CharField(max_length=20, null=True, blank=True)
    sec = models.CharField(max_length=3, null=True, blank=True)
    ray = models.CharField(max_length=3, null=True, blank=True)
    fam = models.CharField(max_length=3, null=True, blank=True)
    sfam = models.CharField(max_length=3, null=True, blank=True)
    marq = models.CharField(max_length=10, null=True, blank=True)
    type_fn = models.CharField(max_length=5, null=True, blank=True)
    dev_fn = models.CharField(max_length=5, null=True, blank=True)
    duree_vie = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=5, null=True, blank=True)
    user_creat = models.CharField(max_length=20, null=True, blank=True)
    date_creat = models.IntegerField(null=True, blank=True)
    date_maj = models.IntegerField(null=True, blank=True)
    user_maj = models.CharField(max_length=50, null=True, blank=True)
    heure_maj = models.IntegerField(null=True, blank=True)
    pcb = models.IntegerField(default=1)
    tva_ach = models.FloatField(default=0.0)
    tva_vte = models.FloatField(default=0.0)
    pds_net = models.FloatField(default=0.0)
    pds_brut = models.FloatField(default=0.0)

    class Meta:
        db_table = 'article'
