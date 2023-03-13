from django.forms import ModelForm
from django.db import models
from ..models.modelsEquip import Pompe

# Déclaration de l'objet chaufferie
class Chaufferie(models.Model):
    #Nombre de chaudière dans la chaufferie
    nbChaudiere = models.IntegerField()
    
    #Déclaration de la liste contenant les objets chaudières
    Chaudieres = []

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

    #Fonction permettant l'ajout des équipements dans l'objet chaudière
    def createEquip(self):
        for chaud in self.Chaudieres:
            chaud.equipements.clear() 
            for i in range(chaud.nbPpe):
                pompe = Pompe('Pompe ' + str(i+1))
                chaud.equipements.append(pompe)
        self.save() #Enregistrement dans la base

#Déclaration de l'objet Chaudière
class Chaudiere(models.Model):
    num = models.IntegerField()
    nomChaud = models.CharField(max_length=200)
    nbBruleur = models.IntegerField()
    nbV2V = models.IntegerField()
    nbPpe = models.IntegerField()
    equipements = [] #Listing des points de la chaudière