from django.shortcuts import render
from .models.modelsChaudiere import Chaufferie
from .models.modelsEquip import Liste
from .forms.formsChaudiere import nbChaudForm, chaudForm
from .ListePTS.listePts import generationListe

#Page 1: Choix de la configuration
def IndexView(request):
    return render(request, 'polls/index.html')
