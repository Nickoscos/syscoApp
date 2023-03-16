from django.shortcuts import render
from .models.modelsChaudiere import Chaufferie
from .models.modelsEquip import Liste
from .forms.formsChaudiere import nbChaudForm, chaudForm
from .ListePTS.listePts import generationListe

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
        c.save()

    #Initialisation de la liste de points
    try:
        #Si l'objet 1 est existant alors on le récupère
        listePts = Liste.objects.get(id=1)
        # liste = Liste.objects.get(id=1)
    except Liste.DoesNotExist:
        #Si l'objet 1 n'existe pas, on ne fait rien
        listePts = Liste.objects.create(id=1)

    ##Déclaration des deux formulaires
    initial_data = c
    nbChaudform = nbChaudForm(request.POST)
    chaudform = chaudForm(request.POST)

    #Détection de l'envoie d'un formulaire
    if request.method == "POST":
        #Choix des actions en fonction du formulaire soumit
        # Soumission du formulaire déterminant le nombre de chaudière
        if (request.POST.get("form_type") == "nbChaudform" and nbChaudform.is_valid()):
            c.nbChaudiere = int(request.POST.get('nbChaudiere')) #Récupération du nombre de chaudières saisies
            Chaufferie.creationChaudiere(c) #Ajout des chaudières dans la base de données
            c = Chaufferie.objects.get(id=1) #Relecture pour affichage
            nbChaudform.save()
        # Soumission du formulaire configuration des chaudières
        elif (request.POST.get("form_type") == "chaudform"): #and chaudform.is_valid()):
            c=Chaufferie.objects.get(id=1) #Relecture pour affichage
            #Modification des chaudières
            # Bouclage en fonction du numéro de la chaudière
            for chaud in c.Chaudieres:
                Chaufferie.updateChaudiere(
                    c,
                    numero=chaud.num,
                    nomChaud=request.POST.get('nomChaud'+str(chaud.num)),
                    nbBruleur=int(request.POST.get('nbBruleur'+str(chaud.num))),
                    nbPpe=int(request.POST.get('nbPpe'+str(chaud.num))),
                    nbV2V=int(request.POST.get('nbV2V'+str(chaud.num))),
                )
            generationListe(c)
    else:
        nbChaudform = nbChaudForm()


    c = Chaufferie.objects.get(id=1) #Relecture pour affichage
    listePts = Liste.objects.get(id=1)
    return render(request, 'polls/chaufferie.html', {
        'nbChaudform': nbChaudform, 
        'chaudform': chaudForm, 
        'chaufferie': c,
        'listePts': listePts
        })