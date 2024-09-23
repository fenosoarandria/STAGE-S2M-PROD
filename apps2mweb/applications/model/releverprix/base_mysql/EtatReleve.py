from django.db import models

class EtatReleve(models.Model):
    id_etat_rel = models.AutoField(primary_key=True)  # Clé primaire auto-incrémentée
    rel_etat_code = models.IntegerField()  # Colonne pour rel_etat_code
    lib_etat_rel = models.CharField(max_length=10)  # Colonne pour lib_etat_rel

    class Meta:
        db_table = 'rel_etat'  # Nom de la table dans la base de données
