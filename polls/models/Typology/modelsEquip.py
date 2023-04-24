from django.db import models


#Déclaration du modèle d'un point
class point(models.Model):
    equip = models.CharField(max_length=200, default='equipement')
    libelle = models.CharField(max_length=200, default='libellé')
    TM = models.IntegerField(default=0)
    TS = models.IntegerField(default=0)
    TR = models.IntegerField(default=0)
    TC = models.IntegerField(default=0)
    Supp = models.BooleanField(default=False)
    
#Déclaration d'une liste de points
class Liste(models.Model):
    pts = []
    user = models.CharField(max_length=200, default="")

        