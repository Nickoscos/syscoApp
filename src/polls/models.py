from django.forms import ModelForm
from django.db import models

# Déclaration de l'objet chaufferie
class Chaufferie(models.Model):
    #Nombre de chaudière dans la chaufferie
    nbChaudiere = models.IntegerField()

    #Déclaration de la liste contenant les objets chaudières
    Chaudiere = []

    # nbPompe = models.IntegerField(max_length=1)
    # nbV2V = models.IntegerField(max_length=1)

    #Fonction permettant de créer les objets chaudières
    def creationChaudiere(self):
        self.Chaudiere.clear()
        for i in range(self.nbChaudiere):
            c = Chaudiere
            c.num = i+1
            print("Chaudière ", c.num)
            self.Chaudiere.append(c)

#Déclaration de l'objet Chaudière
class Chaudiere(models.Model):
    num = 0
    bruleur = models.BooleanField()
    nbPompe = models.IntegerField()
    nbV2V = models.IntegerField()


# Déclaration de la classe du formulaire chaufferie
class ChaufferieForm(ModelForm):
    class Meta:
        model = Chaufferie
        fields = ['nbChaudiere']
        # fields = ['nbChaudiere', 'nbPompe', 'bruleur', 'nbV2V']