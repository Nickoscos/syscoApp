from django.db import models


#Déclaration du modèle d'un point
class point(models.Model):
    libelle = models.CharField(max_length=200)
    TM = models.IntegerField()
    TS = models.IntegerField()
    TR = models.IntegerField()
    TC = models.IntegerField()

    # def ajoutPts(self, libelle, TM, TS, TR, TC):
    #     self.libelle = libelle
    #     self.TM = TM
    #     self.TS = TS
    #     self.TR = TR
    #     self.TC = TC

#Déclaration d'une liste de points
class Liste(models.Model):
    pts = []

        