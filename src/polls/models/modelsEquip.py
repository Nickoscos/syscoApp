from django.db import models


#Déclaration du modèle d'un point
class point(models.Model):
    equip = models.CharField(max_length=200, default='equipement')
    libelle = models.CharField(max_length=200, default='libellé')
    TM = models.IntegerField()
    TS = models.IntegerField()
    TR = models.IntegerField()
    TC = models.IntegerField()
    
#Déclaration d'une liste de points
class Liste(models.Model):
    pts = []

        