from django.db import models

class RayPrep(models.Model):
    rp = models.AutoField(primary_key=True) # Permet des valeurs nulles
    lib_rp = models.CharField(max_length=100, null=True, blank=True)  # Permet des valeurs nulles

    class Meta:
        db_table = 'ray_prep'  # Spécifie le nom de la table dans la base de données
       