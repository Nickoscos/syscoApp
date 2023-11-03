from django.db import models

#Déclaration du modèle des cartes Automate
class carteAutom(models.Model):
    type = models.CharField(max_length=200, default="")
    reference = models.CharField(max_length=200, default="")
    DI = models.IntegerField(default=0)
    DO = models.IntegerField(default=0)
    AI = models.IntegerField(default=0)
    AO = models.IntegerField(default=0)
    UI = models.IntegerField(default=0)
    UO = models.IntegerField(default=0)
    DOR = models.IntegerField(default=0)
    DO_UO = models.IntegerField(default=0)
    nbEmpl = models.IntegerField(default=0)
    extension = models.BooleanField(default=False)
    rs232 = models.IntegerField(default=0)
    rs485 = models.IntegerField(default=0)
    ressources = models.IntegerField(default=0)
    maxModbus = models.IntegerField(default=0)
    Imagerie = models.BooleanField(default=True)
    maxMbus = models.IntegerField(default=0)
    prix = models.FloatField(default=0)


#Déclaration d'une configuration automate
class Automate(carteAutom):
    user = models.CharField(max_length=200, default="")

