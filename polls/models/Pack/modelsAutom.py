from django.db import models

#Déclaration du modèle des cartes Automate
class carteAutom(models.Model):
    type = models.CharField(max_length=200, default="")
    reference = models.CharField(max_length=200, default="", unique=True)
    DI = models.IntegerField()
    DO = models.IntegerField()
    AI = models.IntegerField()
    AO = models.IntegerField()
    UI = models.IntegerField()
    UO = models.IntegerField()
    DOR = models.IntegerField()
    DO_UO = models.IntegerField()
    nbEmpl = models.IntegerField()
    extension = models.BooleanField(default=False)
    rs232 = models.IntegerField()
    rs485 = models.IntegerField()
    ressources = models.IntegerField()
    maxModbus = models.IntegerField()
    Imagerie = models.BooleanField(default=True)
    maxMbus = models.IntegerField()
    prix = models.FloatField()


