from django.forms import ModelForm
from django.db import models

#Déclaration de l'objet Général
class General(models.Model):
    num = models.IntegerField(default=1)
    nomGen = models.CharField(max_length=200, default="Général ")
    nbDefaut = models.IntegerField(default=1)
    nbTempExt = models.IntegerField(default=1)


#Déclaration de l'objet Chaudière
class Chaudiere(models.Model):
    num = models.IntegerField(default=1)
    nomChaud = models.CharField(max_length=200, default="Chaudière " + str(num))
    nbTemp = models.IntegerField(default=2)
    nbDef = models.IntegerField(default=1)
    nbV2V = models.IntegerField(default=1)
    nbPpe = models.IntegerField(default=1)

#Déclaration de l'objet Divers
class Divers(models.Model):
    num = models.IntegerField(default=1)
    nomDivers = models.CharField(max_length=200, default="Divers " + str(num))
    nbV2V = models.IntegerField(default=1)
    nbPpe = models.IntegerField(default=1)
    nbTSsup = models.IntegerField(default=1)

#Déclaration de l'objet ECS
class ECS(models.Model):
    num = models.IntegerField(default=1)
    nomECS = models.CharField(max_length=200, default="ECS " + str(num))
    nbDef = models.IntegerField(default=1)
    nbTemp = models.IntegerField(default=1)
    nbBallon = models.IntegerField(default=1)
    nbV3V = models.IntegerField(default=1)
    nbPpe = models.IntegerField(default=2)

#Déclaration de l'objet Circuit Régulés
class CircReg(models.Model):
    num = models.IntegerField(default=1)
    nomCirc = models.CharField(max_length=200, default="Circuit Régulé " + str(num))
    nbTemp = models.IntegerField(default=1)
    nbAmb = models.IntegerField(default=1)
    nbV3V = models.IntegerField(default=1)
    nbPpe = models.IntegerField(default=2)

#Déclaration de l'objet chaufferie
class Chaufferie(models.Model):
    ######CONFIGURATION GENERAL#####
    #Déclaration de la liste contenant les objets généraux
    General = []

    #Fonction permettant de créer les objets chaudières
    def creationGeneral(self):
        self.General.clear()
        # Initialisation de la liste
        # De base, la liste général comprend: 1 température extérieure, 1 défaut manque d'eau
        self.General.append(General(num=1, nomGen = "Général", nbDefaut = 1, nbTempExt = 1)) 
        self.save() #Enregistrement dans la base

    ######CONFIGURATION CHAUDIERES#####
    #Nombre de chaudière dans la chaufferie
    nbChaudiere = models.IntegerField(default=1)
    
    #Déclaration de la liste contenant les objets chaudières
    Chaudieres = []

    #Fonction permettant de créer les objets chaudières
    def creationChaudiere(self):
        self.Chaudieres.clear()
        for i in range(self.nbChaudiere):
            # Initialisation de la liste de chaudière pour affichage dans le formulaire
            # Le numéro de la chaudière est automatiquement renseignée
            # De base, une chaudière possède : 0 brûleur, 1 pompe, 0 vanne 2 voie
            self.Chaudieres.append(Chaudiere(num = i+1, nomChaud= "Chaudière " + str(i+1), nbTemp=1, nbDef=1, nbV2V=0, nbPpe=1)) 
        self.save() #Enregistrement dans la base

    #Fonction permettant d'actualiser les données chaudières
    def updateChaudiere(self, numero, nomChaud, bruleurPres, nbTemp, nbDef, nbV2V, nbPpe):
        for chaud in self.Chaudieres:
            if chaud.num == numero :
                chaud.nomChaud = nomChaud
                chaud.bruleurPres = bruleurPres
                chaud.nbTemp = nbTemp
                chaud.nbDef = nbDef
                chaud.nbV2V = nbV2V
                chaud.nbPpe = nbPpe
        self.save() #Enregistrement dans la base

    ######CONFIGURATION DIVERS#####
    #Nombre d'équipements divers dans la chaufferie
    nbDivers = models.IntegerField(default=0)

    #Déclaration de la liste contenant les objets chaudières
    Divers = []

    #Fonction permettant de créer les objets divers
    def creationDivers(self):
        self.Divers.clear()
        if self.nbDivers > 0 :
            for i in range(self.nbDivers):
                # Initialisation de la liste des équipements divers pour affichage dans le formulaire
                # Le numéro de l'équipement divers est automatiquement renseignée
                # De base, une équipement divers possède : 1 TS, 1 pompe, 0 vanne 2 voie
                self.Divers.append(Divers(num = i+1, nomDivers= "Divers " + str(i+1), nbTSsup = 0, nbV2V=0, nbPpe=1)) 
            self.save() #Enregistrement dans la base

    #Fonction permettant d'actualiser les données des équipements divers
    def updateDivers(self, numero, nomDivers, nbTSsup, nbV2V, nbPpe):
        for divers in self.Divers:
            if divers.num == numero :
                divers.nomDivers = nomDivers
                divers.nbTSsup = nbTSsup
                divers.nbV2V = nbV2V
                divers.nbPpe = nbPpe
        self.save() #Enregistrement dans la base

    ######CONFIGURATION CIRCUITS REGULES#####
    #Nombre de circuits régulés dans la chaufferie
    nbCircReg = models.IntegerField(default=1)

    #Déclaration de la liste contenant les objets circuits régulés
    CircReg = []

    #Fonction permettant de créer les objets circuits régulés
    def creationCircReg(self):
        self.CircReg.clear()
        for i in range(self.nbCircReg):
            # Initialisation de la liste de circuits régulés pour affichage dans le formulaire
            # Le numéro du circuit régulé est automatiquement renseignée
            # De base, un circuit régulé possède : 1 Mesure de température, 1 pompe, 1 vanne 3 voie
            self.CircReg.append(CircReg(num = i+1, nomCirc= "Circuit Régulé " + str(i+1), nbTemp = 1, nbAmb = 1, nbV3V=1, nbPpe=1)) 
        self.save() #Enregistrement dans la base

    #Fonction permettant d'actualiser les données circuit régulé
    def updateCircReg(self, numero, nomCirc, nbTemp, nbAmb, nbV3V, nbPpe):
        for circ in self.CircReg:
            if circ.num == numero :
                circ.nomCirc = nomCirc
                circ.nbTemp = nbTemp
                circ.nbAmb = nbAmb
                circ.nbV3V = nbV3V
                circ.nbPpe = nbPpe
        self.save() #Enregistrement dans la base
    
    ######CONFIGURATION ECS#####
    #L'ECS est-il présent:
    ECSpres = models.BooleanField(default=False)
    #L'ECS possède-t-il un préparateur indépendant:
    ECSprepa = models.BooleanField(default=True)

    ECS = []

    #Fonction permettant de créer les objets circuits constants
    def creationECS(self):
        self.ECS.clear()
        if (self.ECSpres and not self.ECSprepa) :
        # Initialisation de la liste de circuits constants pour affichage dans le formulaire
        # Le numéro du circuit régulé est automatiquement renseignée
        # De base, un circuit régulé possède : 1 Mesure de température, 2 pompes, 1 vanne 3 voie
            self.ECS.append(ECS(num = 1, nomECS= "ECS " + str(1), nbDef=1, nbTemp=2, nbBallon=1, nbPpe=1, nbV3V=1)) 
        elif (self.ECSpres and self.ECSprepa) :
            self.ECS.append(ECS(num = 1, nomECS= "ECS " + str(1), nbDef=1, nbTemp=2, nbBallon=0, nbPpe=0, nbV3V=0)) 
        self.save() #Enregistrement dans la base

    #Fonction permettant d'actualiser les données ECS
    def updateECS(self, nomECS, nbDef, nbTemp, nbBallon, nbPpe, nbV3V):
        self.ECS[0].nomECS = nomECS
        self.ECS[0].nbTemp = nbTemp
        self.ECS[0].nbDef = nbDef
        self.ECS[0].nbPpe = nbPpe
        self.ECS[0].nbBallon = nbBallon
        self.ECS[0].nbV3V = nbV3V
        self.save() #Enregistrement dans la base

    #Déclaration de la liste des points
    listePts = []


