from django.shortcuts import render
from ..models.Typology.modelsChaudiere import Chaufferie
from ..models.Typology.modelsEquip import Liste
from ..forms.formsChaudiere import nbChaudForm, chaudForm
from ..ListePTS.listePts import generationListe, updateListe, generationXls

#Page 2: Définition de la configuration de la chaufferie 
def chaufferieView(request,part_id =None):
    message = "" 
    #Création d'un unique objet chaufferie dans la base de données 
    try:
        #Si l'objet 1 est existant alors on le récupère
        c = Chaufferie.objects.get(id=1)
    except Chaufferie.DoesNotExist:
        #Si l'objet 1 n'existe pas, on l'initialise
        c = Chaufferie.objects.create(id=1, nbChaudiere=1, nbDivers=0)
        c.save()

    #Initialisation de la liste de points
    try:
        #Si l'objet 1 est existant alors on le récupère
        listePts = Liste.objects.get(id=1)
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
            message = "Générer la liste de points" 
            c.nbChaudiere = int(request.POST.get('nbChaudiere')) #Récupération du nombre de chaudières saisies
            c.nbDivers = int(request.POST.get('nbDivers')) #Récupération du nombre de chaudières saisies
            c.nbCircReg = int(request.POST.get('nbCircReg')) #Récupération du nombre de circuits régulés saisies
            c.ECSpres = bool(request.POST.get('ECSpres'))
            c.ECSprepa = bool(request.POST.get('ECSprepa'))

            Chaufferie.creationGeneral(c) #Ajout partie générale dans la base de données
            Chaufferie.creationChaudiere(c) #Ajout des chaudières dans la base de données
            Chaufferie.creationDivers(c) #Ajout des équipements Divers dans la base de données
            Chaufferie.creationCircReg(c) #Ajout des circuits régulés dans la base de données
            Chaufferie.creationECS(c) #Ajout de l'ECS dans la base de données       

            c = Chaufferie.objects.get(id=1) #Relecture pour affichage
            nbChaudform.save()

        # Soumission du formulaire configuration des équipements
        elif (request.POST.get("form_type") == "chaudform"): #and chaudform.is_valid()):
            c=Chaufferie.objects.get(id=1) #Relecture pour affichage
            #Modification des chaudières
            # Bouclage en fonction du numéro de la chaudière
            for chaud in c.Chaudieres:
                Chaufferie.updateChaudiere(
                    c,
                    numero=chaud.num,
                    nomChaud=request.POST.get('nomChaud'+str(chaud.num)),
                    bruleurPres=bool(request.POST.get('bruleurPres'+str(chaud.num))),
                    nbTemp=int(request.POST.get('nbTemp'+str(chaud.num))),
                    nbDef=int(request.POST.get('nbDef'+str(chaud.num))),
                    nbPpe=int(request.POST.get('nbPpeChaud'+str(chaud.num))),
                    nbV2V=int(request.POST.get('nbV2VChaud'+str(chaud.num))),
                )
            # Bouclage en fonction du numéro de la chaudière
            for divers in c.Divers:
                Chaufferie.updateDivers(
                    c,
                    numero=divers.num,
                    nomDivers=request.POST.get('nomDivers'+str(divers.num)),
                    nbTSsup=int(request.POST.get('nbTSsupDivers'+str(divers.num))),
                    nbPpe=int(request.POST.get('nbPpeDivers'+str(divers.num))),
                    nbV2V=int(request.POST.get('nbV2VDivers'+str(divers.num))),
                )
            # Bouclage en fonction du numéro du circuit régulé
            for circ in c.CircReg:
                Chaufferie.updateCircReg(
                    c,
                    numero=circ.num,
                    nomCirc=request.POST.get('nomCircReg'+str(circ.num)),
                    nbTemp=int(request.POST.get('nbTempCircReg'+str(circ.num))),
                    nbAmb=int(request.POST.get('nbAmbCircReg'+str(circ.num))),
                    nbPpe=int(request.POST.get('nbPpeCircReg'+str(circ.num))),
                    nbV3V=int(request.POST.get('nbV3VCircReg'+str(circ.num))),
                )
            # Bouclage en fonction du numéro de l'ECS
            for ECS in c.ECS:
                Chaufferie.updateECS(
                    c,
                    nomECS=request.POST.get('nomECS'+str(ECS.num)),
                    nbBallon=int(request.POST.get('nbBallonECS'+str(ECS.num))),
                    nbV3V=int(request.POST.get('nbV3VECS'+str(ECS.num))),
                    nbDef=int(request.POST.get('nbDef'+str(ECS.num))),
                    nbTemp=int(request.POST.get('nbTempECS'+str(ECS.num))),
                    nbPpe=int(request.POST.get('nbPpeECS'+str(ECS.num))),
                )

            message = generationListe(c)
        elif (request.POST.get("form_type") == "listform"):
            message = updateListe(listePts, request)

        # Soumission du formulaire de téléchargement liste de point
        elif (request.POST.get("form_type") == "downloadListTemplate"): #and chaudform.is_valid()):
            print("téléchargement")
            try:
                #Si l'objet 2 est existant alors on le récupère
                cTemplate = Chaufferie.objects.get(id=2)
            except Chaufferie.DoesNotExist:
                #Si l'objet 1 n'existe pas, on l'initialise
                cTemplate = Chaufferie.objects.create(id=2, nbChaudiere=1, nbDivers=0)
                cTemplate.save()

            cTemplate.nbDivers = 0
            cTemplate.nbCircReg = 1
            cTemplate.ECSpres = False
            cTemplate.ECSprepa = False

            Chaufferie.creationGeneral(cTemplate) #Ajout partie générale dans la base de données
            Chaufferie.creationChaudiere(cTemplate) #Ajout des chaudières dans la base de données
            Chaufferie.creationDivers(cTemplate) #Ajout des équipements Divers dans la base de données
            Chaufferie.creationCircReg(cTemplate) #Ajout des circuits régulés dans la base de données
            Chaufferie.creationECS(cTemplate) #Ajout de l'ECS dans la base de données       

            cTemplate = Chaufferie.objects.get(id=2) #Relecture pour affichage

            cTemplate.save()
            generationListe(cTemplate)

        # Soumission du formulaire de téléchargement liste de point
        elif (request.POST.get("form_type") == "exportExcelList"):
            message = generationXls(listePts)

        # Soumission du formulaire permettant la suppresion d'une ligne de la liste de points
        elif (request.POST.get("form_type") == "deleteForm"): #and chaudform.is_valid()):
            print("Suppression " + request.POST.get('Supp'))
            print(listePts.pts[int(request.POST.get('Supp'))].libelle)
            listePts.pts.pop(int(request.POST.get('Supp')))
    else:
        nbChaudform = nbChaudForm()

    if part_id != None :
        print('test')
        listPt_select = listePts.pts[part_id]
        listPt_select.delete()

    c = Chaufferie.objects.get(id=1) #Relecture pour affichage
    listePts = Liste.objects.get(id=1)
    return render(request, 'polls/chaufferie.html', {
        'nbChaudform': nbChaudform, 
        'chaudform': chaudForm, 
        'chaufferie': c,
        'listePts': listePts,
        'message': message
        })
