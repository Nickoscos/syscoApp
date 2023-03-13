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
        print("Récupération et le nombre de chaudière est de ", c.Chaudieres)
    except Chaufferie.DoesNotExist:
        #Si l'objet 1 n'existe pas, on l'initialise
        c = Chaufferie.objects.create(id=1, nbChaudiere=1)
        c.save()
        print("Création")
    ##Déclaration des deux formulaires
    initial_data = c
    nbChaudform = nbChaudForm(request.POST)

    #Détection de l'envoie d'un formulaire
    if request.method == "POST":
        # nbChaudform = nbChaudForm(request.POST)
        chaudform = chaudForm(request.POST)
        #Choix des actions en fonction du formulaire soumit
        # Soumission du formulaire déterminant le nombre de chaudière
        if (request.POST.get("form_type") == "nbChaudform" and nbChaudform.is_valid()):
            c.nbChaudiere = int(request.POST.get('nbChaudiere')) #Récupération du nombre de chaudières saisies
            Chaufferie.creationChaudiere(c) #Ajout des chaudières dans la base de données
            c.save() #Enregistrement dans la base
            c = Chaufferie.objects.get(id=1) #Relecture pour affichage

        # Soumission du formulaire configuration des chaudières
        elif (request.POST.get("form_type") == "chaudform" and chaudform.is_valid()):
            c=Chaufferie.objects.get(id=1) #Relecture pour affichage
            #Modification de la chaudière
            Chaufferie.updateChaudiere(
                c,
                numero=int(1),
                nomChaud=request.POST.get('nomChaud'),
                nbBruleur=int(request.POST.get('nbBruleur')),
                nbPpe=int(request.POST.get('nbPpe')),
                nbV2V=int(request.POST.get('nbV2V')),
            )
            c.save()
    else:
        nbChaudform = nbChaudForm()

    c = Chaufferie.objects.get(id=1) #Relecture pour affichage
    return render(request, 'polls/chaufferie.html', {'nbChaudform': nbChaudform, 'chaudform': chaudForm, 'chaufferie': c})