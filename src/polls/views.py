from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader

from .models import Chaufferie
from .forms import nbChaudForm, chaudForm

#Page 1: Choix de la configuration
def IndexView(request):
    return render(request, 'polls/index.html')

#Page 2: Définition de la configuration de la chaufferie 
def chaufferieView(request):
    
    #Création d'un unique objet chaufferie dans la base de données 
    try:
        #Si l'objet 1 est existant alors on le récupère
        c = Chaufferie.objects.get(id=1)
    except Chaufferie.DoesNotExist:
        #Si l'objet 1 n'existe pas, on l'initialise
        c = Chaufferie.objects.create(id=1, nbChaudiere=1)

    ##Déclaration des deux formulaires
    print(c.nbChaudiere)
    initial_data = c
    nbChaudform = nbChaudForm(request.POST or None)
    print(nbChaudform['nbChaudiere'].value())

    #Détection de l'envoie d'un formulaire
    if request.method == "POST":
        # nbChaudform = nbChaudForm(request.POST)
        chaudform = chaudForm(request.POST)
        #Choix des actions en fonction du formulaire soumit
        # Soumission du formulaire déterminant le nombre de chaudière
        if (request.POST.get("form_type") == "nbChaudform" and nbChaudform.is_valid()):
            c.nbChaudiere = int(request.POST.get('nbChaudiere')) #Récupération du nombre de chaudières saisies
            Chaufferie.creationChaudiere(c) #Ajout des chaudières dans la base de données
            nbChaudform.save()
        # Soumission du formulaire configuration des chaudières
        elif (request.POST.get("form_type") == "chaudform" and chaudform.is_valid()):
            print('enregistrement chaudière')

    else:
        nbChaudform = nbChaudForm()

    return render(request, 'polls/chaufferie.html', {'nbChaudform': nbChaudform, 'chaudform': chaudForm, 'chaufferie': c})