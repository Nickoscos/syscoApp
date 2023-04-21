from django import forms
from ..models.Typology.modelsChaudiere import Chaufferie, Chaudiere

#Formulaire définissant le nombre de chaudières composant la chaufferie
class nbChaudForm(forms.ModelForm):
  class Meta:
    model = Chaufferie
    fields = ["nbChaudiere"]
    labels = {'nbChaudiere': "Nombre Chaudières"}

#Formulaire définissant les éléments qui composent chaque chaudière
class chaudForm(forms.ModelForm):
  class Meta:
    model = Chaudiere
    fields = ["nomChaud","nbPpe", "nbV2V"]
    labels = {'nomChaud': "Nom", 'nbPpe': "Nombre de pompes", 'nbV2V':"Nombre de V2V"}