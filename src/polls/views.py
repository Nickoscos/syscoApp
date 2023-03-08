from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader

from .models import Chaufferie

#Page 1: Choix de la configuration
def IndexView(request):
    return render(request, 'polls/index.html')

#Page 2: Définition de la configuration de la chaufferie
def ChaufferieView(request):

    #Création d'un unique objet chaufferie dans la base de données 
    try:
        #Si l'objet 1 est existant alors on le récupère
        c = Chaufferie.objects.get(id=1)
    except Chaufferie.DoesNotExist:
        #Si l'objet 1 n'existe pas, on l'initialise
        c = Chaufferie.objects.create(id=1, nbChaudiere=1)

    #Ajout des chaudières
    Chaufferie.creationChaudiere(c)

    #On renvoie les données vers la page
    chaufferie = Chaufferie.objects.order_by('id')
    print(chaufferie[0].nbChaudiere)
    context = { 'chaufferie': chaufferie[0] }
    return render(request, 'polls/chaufferie.html' , context)
    # return render(request, 'polls/chaufferie.html', {'chaufferie': chaufferie})


