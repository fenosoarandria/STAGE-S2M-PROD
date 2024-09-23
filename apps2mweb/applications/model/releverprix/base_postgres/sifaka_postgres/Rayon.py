from django.db import models

class Rayon(models.Model):
    rayon = models.CharField(max_length=255, primary_key=True)  # Clé primaire de type VARCHAR
    rayl30c = models.CharField(max_length=255)
    sectray = models.CharField(max_length=255)

    class Meta:
        db_table = 'rayon'
