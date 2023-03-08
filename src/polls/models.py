from django.forms import ModelForm
from django.db import models

# Déclaration de l'objet chaufferie
class Chaufferie(models.Model):
    #Nombre de chaudière dans la chaufferie
    nbChaudiere = models.IntegerField(max_length=1)

    # nbPompe = models.IntegerField(max_length=1)
    # bruleur = models.BooleanField()
    # nbV2V = models.IntegerField(max_length=1)

# Déclaration de la classe du formulaire chaufferie
class ChaufferieForm(ModelForm):
    class Meta:
        model = Chaufferie
        fields = ['nbChaudiere']
        # fields = ['nbChaudiere', 'nbPompe', 'bruleur', 'nbV2V']