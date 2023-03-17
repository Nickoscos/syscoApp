from django.forms import ModelForm
from django.db import models

#Déclaration de l'objet Chaudière
class Chaudiere(models.Model):
    num = models.IntegerField(default=1)
    nomChaud = models.CharField(max_length=200, default="Chaudière " + str(num))
    nbBruleur = models.IntegerField(default=0)
    nbV2V = models.IntegerField(default=1)
    nbPpe = models.IntegerField(default=1)

#Déclaration de l'objet Divers
class Divers(models.Model):
    num = models.IntegerField(default=1)
    nomDivers = models.CharField(max_length=200, default="Divers " + str(num))
    nbV2V = models.IntegerField(default=1)
    nbPpe = models.IntegerField(default=1)
    nbTSsup = models.IntegerField(default=1)


#Déclaration de l'objet chaufferie
class Chaufferie(models.Model):
    #Nombre de chaudière dans la chaufferie
    nbChaudiere = models.IntegerField(default=1)

    #Nombre d'équipements divers dans la chaufferie
    nbDivers = models.IntegerField(default=0)
    
    #Déclaration de la liste contenant les objets chaudières
    Chaudieres = []

    #Déclaration de la liste contenant les objets chaudières
    Divers = []

    #Déclaration de la liste des points
    listePts = []

    ###### CHAUDIERES ########
    #Fonction permettant de créer les objets chaudières
    def creationChaudiere(self):
        self.Chaudieres.clear()
        for i in range(self.nbChaudiere):
            # Initialisation de la liste de chaudière pour affichage dans le formulaire
            # Le numéro de la chaudière est automatiquement renseignée
            # De base, une chaudière possède : 0 brûleur, 1 pompe, 1 vanne 2 voie
            self.Chaudieres.append(Chaudiere(num = i+1, nomChaud= "Chaudière " + str(i+1), nbBruleur = 0, nbV2V=1, nbPpe=1)) 
        self.save() #Enregistrement dans la base

    #Fonction permettant d'actualiser les données chaudières
    def updateChaudiere(self, numero, nomChaud, nbBruleur, nbV2V, nbPpe):
        for chaud in self.Chaudieres:
            if chaud.num == numero :
                chaud.nomChaud = nomChaud
                chaud.nbBruleur = nbBruleur
                chaud.nbV2V = nbV2V
                chaud.nbPpe = nbPpe
        self.save() #Enregistrement dans la base

    ###### DIVERS ########
    #Fonction permettant de créer les objets divers
    def creationDivers(self):
        self.Divers.clear()
        if self.nbDivers > 0 :
            for i in range(self.nbDivers):
                # Initialisation de la liste des équipements divers pour affichage dans le formulaire
                # Le numéro de l'équipement divers est automatiquement renseignée
                # De base, une équipement divers possède : 1 TS, 1 pompe, 0 vanne 2 voie
                self.Divers.append(Divers(num = i+1, nomDivers= "Divers " + str(i+1), nbTSsup = 0, nbV2V=1, nbPpe=1)) 
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
