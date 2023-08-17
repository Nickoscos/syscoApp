from django.db import models


#Déclaration du modèle d'un point
class point(models.Model):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)  
    # def __init__(self, equip, libelle, type, TM, TS, TR, TC, Supp):
    #     self.equip = equip
    #     self.libelle = libelle
    #     self.type = type
    #     self.TM = TM
    #     self.TR = TR
    #     self.TS = TS
    #     self.TC = TC
    #     self.Supp = Supp

    equip = models.CharField(max_length=200, default='equipement')
    libelle = models.CharField(max_length=200, default='libellé')
    type = models.CharField(max_length=200, default='')
    TM = models.IntegerField(default=0)
    TS = models.IntegerField(default=0)
    TR = models.IntegerField(default=0)
    TC = models.IntegerField(default=0)
    Supp = models.BooleanField(default=False)

    
#Déclaration d'une liste de points
class Liste(models.Model):
    def __init__(self, user):
        super().__init__(user)

    pts = [models.ForeignKey(point,on_delete=models.CASCADE)]
    user = models.CharField(max_length=200, default="")


class Temp(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Température '
        self.type = "Temp"
        self.TM = 1
        self.TS = 0
        self.TR = 0
        self.TC = 0
        self.Supp = False

class Amb(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Température Ambiant'
        self.type = "Amb"
        self.TM = 1
        self.TS = 0
        self.TR = 0
        self.TC = 0
        self.Supp = False

class SyntDefaut(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Synthèse défaut '
        self.type = "SynthDef"
        self.TM = 0
        self.TS = 1
        self.TR = 0
        self.TC = 0
        self.Supp = False

class DefPpe(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Défaut pompe '
        self.type = "DefPpe"
        self.TM = 0
        self.TS = 1
        self.TR = 0
        self.TC = 0
        self.Supp = False

class CmdPpe(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Commande pompe '
        self.type = "CmdPpe"
        self.TM = 0
        self.TS = 0
        self.TR = 1
        self.TC = 1
        self.Supp = False

class CmdChaud(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Commande chaudiere '
        self.type = "CmdChaud"
        self.TM = 0
        self.TS = 0
        self.TR = 0
        self.TC = 1
        self.Supp = False

class CmdV3V(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Commande V3V '
        self.type = "CmdV3V"
        self.TM = 0
        self.TS = 0
        self.TR = 1
        self.TC = 0
        self.Supp = False

class CmdV2V(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Commande V2V '
        self.type = "CmdV2V"
        self.TM = 0
        self.TS = 0
        self.TR = 0
        self.TC = 1
        self.Supp = False

class FdcV2V(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Fin de course V2V '
        self.type = "FdcV2V"
        self.TM = 0
        self.TS = 1
        self.TR = 0
        self.TC = 0
        self.Supp = False

class Info(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Information supplémentaire '
        self.type = "Info"
        self.TM = 0
        self.TS = 1
        self.TR = 0
        self.TC = 0
        self.Supp = False

class CmdBal(point):
    def __init__(self, equip):
        self.equip = equip
        self.libelle = 'Commande Epingle Ballon '
        self.type = "CmdBal"
        self.TM = 0
        self.TS = 0
        self.TR = 0
        self.TC = 1
        self.Supp = False
