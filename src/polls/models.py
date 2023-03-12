from django.forms import ModelForm
from django.db import models

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
            self.Chaudieres.append(Chaudiere(i+1, "Chaudière " + str(i+1),0, 1, 1)) 


#Déclaration de l'objet Chaudière
class Chaudiere(models.Model):
    num = models.IntegerField()
    nomChaud = models.CharField(max_length=20)
    nbBruleur = models.IntegerField()
    nbV2V = models.IntegerField()
    nbPpe = models.IntegerField()