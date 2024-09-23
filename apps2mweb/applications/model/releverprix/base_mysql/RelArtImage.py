from django.db import models

class RelArtImage(models.Model):
    id = models.AutoField(primary_key=True)  # Clé primaire auto-incrémentée
    id_art_concur = models.IntegerField()  # Correspond à `id_art_concur` dans la table MySQL
    image_art = models.CharField(max_length=255)  # Correspond à `image_art`

    class Meta:
        db_table = 'rel_art_image'  # Assure que Django utilise la même table MySQL

