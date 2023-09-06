from django.db import models

#Déclaration du modèle d'un PACK TELEGESTION
class PackTG(models.Model):
    Reference = models.CharField(max_length=200, default="", unique=True)
    AI = models.IntegerField()
    DI = models.IntegerField()
    AO = models.IntegerField()
    DO = models.IntegerField()
    priceWIT = models.FloatField()
    priceTREND = models.FloatField()
    priceDISTECH = models.FloatField()
    priceSOFREL = models.FloatField()
    priceMOY = models.FloatField()

#Déclaration du modèle d'un PACK OPTIMISATION IOT
class PackOPT(models.Model):
    Reference = models.CharField(max_length=200, default="", unique=True)
    nbIOTmax = models.IntegerField()
    Tamb = models.IntegerField()
    TECS = models.IntegerField()
    pricePAS = models.FloatField()
    priceTamb = models.FloatField()
    priceTECS = models.FloatField()
    priceTOT = models.FloatField()

#Déclaration du modèle d'un PACK IOT
class PackIOTUnit(models.Model):
    Reference = models.CharField(max_length=200, default="", unique=True)
    type = models.CharField(max_length=200, default="")
    comment = models.CharField(max_length=200, default="")
    price = models.FloatField()

#Déclaration d'une liste de points
class listePacks(models.Model):
    num = models.IntegerField(default=1)
    pack = []

