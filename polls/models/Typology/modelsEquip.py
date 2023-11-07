from django.db import models


#Déclaration d'une liste de points
class Liste(models.Model):
    # pts = [models.ForeignKey(point,on_delete=models.CASCADE)]
    user = models.CharField(max_length=200, default="")

#Déclaration du modèle d'un point
class Point(models.Model):
    equip = models.CharField(max_length=200, default='equipement')
    libelle = models.CharField(max_length=200, default='libellé')
    type = models.CharField(max_length=200, default='')
    TM = models.IntegerField(default=0)
    TS = models.IntegerField(default=0)
    TR = models.IntegerField(default=0)
    TC = models.IntegerField(default=0)
    Supp = models.BooleanField(default=False)
    user = models.CharField(max_length=200, default="")


#Déclaration du modèle LotIOT
class LotIOT(models.Model):
    user = models.CharField(max_length=200, default="")
    Passerelle = models.BooleanField(default=True)
    nbTempAmbIOT = models.IntegerField(default=0)
    nbTemp1EauIOT = models.IntegerField(default=0)
    nbTemp2EauIOT = models.IntegerField(default=0)
    nbCO2IOT = models.IntegerField(default=0)
    nbTLRGazIOT = models.IntegerField(default=0)
    nbTLREauIOT = models.IntegerField(default=0)
    nbTLRElecIOT = models.IntegerField(default=0)
    nbTLRCaloIOT = models.IntegerField(default=0)

class Temp(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Température '
        self.type = "Temp"
        self.TM = 1
        self.TS = 0
        self.TR = 0
        self.TC = 0
        self.Supp = False
        self.username = username

class Amb(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Température Ambiant'
        self.type = "Amb"
        self.TM = 1
        self.TS = 0
        self.TR = 0
        self.TC = 0
        self.Supp = False
        self.username = username

class SyntDefaut(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Synthèse défaut '
        self.type = "SynthDef"
        self.TM = 0
        self.TS = 1
        self.TR = 0
        self.TC = 0
        self.Supp = False
        self.username = username

class DefPpe(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Défaut pompe '
        self.type = "DefPpe"
        self.TM = 0
        self.TS = 1
        self.TR = 0
        self.TC = 0
        self.Supp = False
        self.username = username

class CmdPpe(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Commande pompe '
        self.type = "CmdPpe"
        self.TM = 0
        self.TS = 0
        self.TR = 1
        self.TC = 1
        self.Supp = False
        self.username = username

class CmdChaud(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Commande chaudiere '
        self.type = "CmdChaud"
        self.TM = 0
        self.TS = 0
        self.TR = 0
        self.TC = 1
        self.Supp = False
        self.username = username

class CmdV3V(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Commande V3V '
        self.type = "CmdV3V"
        self.TM = 0
        self.TS = 0
        self.TR = 1
        self.TC = 0
        self.Supp = False
        self.username = username

class CmdV2V(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Commande V2V '
        self.type = "CmdV2V"
        self.TM = 0
        self.TS = 0
        self.TR = 0
        self.TC = 1
        self.Supp = False
        self.username = username

class FdcV2V(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Fin de course V2V '
        self.type = "FdcV2V"
        self.TM = 0
        self.TS = 1
        self.TR = 0
        self.TC = 0
        self.Supp = False
        self.username = username

class Info(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Information supplémentaire '
        self.type = "Info"
        self.TM = 0
        self.TS = 1
        self.TR = 0
        self.TC = 0
        self.Supp = False
        self.username = username

class CmdBal(Point):
    def __init__(self, equip, username):
        self.equip = equip
        self.libelle = 'Commande Epingle Ballon '
        self.type = "CmdBal"
        self.TM = 0
        self.TS = 0
        self.TR = 0
        self.TC = 1
        self.Supp = False
        self.username = username
