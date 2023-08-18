from django.db import models

#Déclaration du modèle d'un PACK
class Pack(models.Model):
    # id = models.IntegerField()
    Reference = models.CharField(max_length=200, default="")
    AI = models.IntegerField()
    DI = models.IntegerField()
    AO = models.IntegerField()
    DO = models.IntegerField()
    priceWIT = models.FloatField()
    priceTREND = models.FloatField()
    priceDISTECH = models.FloatField()
    priceSOFREL = models.FloatField()
    priceMOY = models.FloatField()

#Déclaration d'une liste de points
class listePacks(models.Model):
    id = models.IntegerField(default=1, primary_key=True)
    pack = []

