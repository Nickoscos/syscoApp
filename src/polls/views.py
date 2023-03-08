from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

from .models import Chaufferie

#Page 1: Choix de la configuration
def IndexView(request):
    return render(request, 'polls/index.html')

#Page 2: Définition de la configuration de la chaufferie
def ChaufferieView(request):

    #Création d'un unique objet chaufferie dans la base de données 
    try:
        #Si l'objet 1 est existant alors on le récupère
        Chaufferie.objects.get(id=1)
    except Chaufferie.DoesNotExist:
        #Si l'objet 1 n'existe pas, on l'initialise
        Chaufferie.objects.create(id=1, nbChaudiere=1)

    #On renvoie les données vers la page
    chaufferie = get_object_or_404(Chaufferie)
    return render(request, 'polls/chaufferie.html', {'chaufferie': chaufferie})
