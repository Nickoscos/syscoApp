from django.shortcuts import render
from django.shortcuts import redirect

from ..ListePTS.export import upload_file
from ..models.Typology.modelsChaudiere import Chaufferie
from ..models.Typology.modelsEquip import LotIOT
from ..forms.formsChaudiere import nbChaudForm, chaudForm
from ..ListePTS.listePts import generationListe, updateListe, generationXls, calculTotaux, RAZListe
from ..models.Typology.modelsEquip import Point
from ..models.Pack.modelsPacks import PackTG, PackOPT, PackIOTUnit


#GENERATION DE LA LISTE DE POINTS
def genListeView(request):
    message = "" 

    # if request.user.username != "":
    #Création d'un unique objet chaufferie dans la base de données  
    try:
        #Si l'objet 1 est existant alors on le récupère
        c = Chaufferie.objects.get(user=request.user.username)
    except Chaufferie.DoesNotExist:
        #Si l'objet 1 n'existe pas, on l'initialise
        print("create")
        c = Chaufferie.objects.create(user=request.user.username, nbChaudiere=1, nbDivers=0)
        c.save()

    #Création d'un unique objet IOT dans la base de données  
    try:
        #Si l'objet 1 est existant alors on le récupère
        iot = LotIOT.objects.get(user=request.user.username)
    except LotIOT.DoesNotExist:
        #Si l'objet 1 n'existe pas, on l'initialise
        print("create")
        iot = LotIOT.objects.create(user=request.user.username)
        iot.save()


    ##Déclaration du formulaire
    nbChaudform = nbChaudForm(request.POST)


    #Détection de l'envoie d'un formulaire
    if request.method == "POST":
        # Choix des actions en fonction du formulaire soumit
        # Soumission du formulaire déterminant le nombre de chaudières
        if (request.POST.get("form_type") == "nbChaudform"):
            message = "Ajuster le nombre de points puis générer liste de points" 
            c.nomInstal = request.POST.get('nomInstal') #Récupération du nombre de chaudières saisies
            c.nbChaudiere = int(request.POST.get('nbChaudiere')) #Récupération du nombre de chaudières saisies
            c.nbMbus = int(request.POST.get('nbMbus')) #Récupération du nombre de compteurs Mbus saisies
            c.nbModbus = int(request.POST.get('nbModbus')) #Récupération du nombre de compteurs Modbus saisies
            c.nbImp = int(request.POST.get('nbImp')) #Récupération du nombre de compteurs impulsionnels saisies
            c.nbDivers = int(request.POST.get('nbDivers')) #Récupération du nombre de chaudières saisies
            c.nbCircReg = int(request.POST.get('nbCircReg')) #Récupération du nombre de circuits régulés saisies
            c.ECSpres = bool(request.POST.get('ECSpres'))
            c.ECSprepa = bool(request.POST.get('ECSprepa'))
            c.modemNec = bool(request.POST.get('modemNec'))
            c.nbPortModem = int(request.POST.get('nbPortModem'))
            c.ecranNec = bool(request.POST.get('ecranNec'))

            Chaufferie.creationGeneral(c) #Ajout partie générale dans la base de données
            Chaufferie.creationChaudiere(c) #Ajout des chaudières dans la base de données
            Chaufferie.creationDivers(c) #Ajout des équipements Divers dans la base de données
            Chaufferie.creationCircReg(c) #Ajout des circuits régulés dans la base de données
            Chaufferie.creationECS(c) #Ajout de l'ECS dans la base de données       

        # Soumission du formulaire configuration des équipements
        elif (request.POST.get("form_type") == "chaudform"): #and chaudform.is_valid()):
            c=Chaufferie.objects.get(user=request.user.username) #Relecture pour affichage
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

            iot.Passerelle = bool(request.POST.get('Passerelle'))
            iot.nbTempAmbIOT = int(request.POST.get('nbTempAmbIOT'))
            iot.nbTemp1EauIOT = int(request.POST.get('nbTemp1EauIOT'))
            iot.nbTemp2EauIOT = int(request.POST.get('nbTemp2EauIOT'))
            iot.nbCO2IOT = int(request.POST.get('nbCO2IOT'))
            iot.nbTLRGazIOT = int(request.POST.get('nbTLRGazIOT'))
            iot.nbTLREauIOT = int(request.POST.get('nbTLREauIOT'))
            iot.nbTLRElecIOT = int(request.POST.get('nbTLRElecIOT'))
            iot.nbTLRCaloIOT = int(request.POST.get('nbTLRCaloIOT'))
            iot.save()

            message = generationListe(request, c)
            return redirect("polls:config")
        
        elif (request.POST.get("form_type") == "RAZ"):
            print("test")
            message = "Ajuster le nombre de points puis générer liste de points" 
            c.nomInstal = "Nouvelle installation" #Récupération du nombre de chaudières saisies
            c.nbChaudiere = 0 #Récupération du nombre de chaudières saisies
            c.nbDivers = 0 #Récupération du nombre de chaudières saisies
            c.nbCircReg = 0 #Récupération du nombre de circuits régulés saisies
            c.ECSpres = False
            c.ECSprepa = False
            c.modemNec = True
            c.nbPortModem = 5
            c.ecranNec = True

            Chaufferie.creationGeneral(c) #Ajout partie générale dans la base de données
            Chaufferie.creationChaudiere(c) #Ajout des chaudières dans la base de données
            Chaufferie.creationDivers(c) #Ajout des équipements Divers dans la base de données
            Chaufferie.creationCircReg(c) #Ajout des circuits régulés dans la base de données
            Chaufferie.creationECS(c) #Ajout de l'ECS dans la base de données       

            LotIOT.objects.get(user=request.user.username).delete()


    c = Chaufferie.objects.get(user=request.user.username) #Relecture pour affichage

    return render(request, 'polls/chaufferie.html', {
        'nbChaudform': nbChaudform, 
        'chaudform': chaudForm, 
        'chaufferie': c,
        'LotIOT': iot,
        'message': message
        })

#Page 2: AFFICHAGE LISTE DE POINTS
def listePts(request):
    message = "" 
    #Création d'un unique objet chaufferie dans la base de données 
    try:
        #Si l'objet 1 est existant alors on le récupère
        c = Chaufferie.objects.get(user=request.user.username)
    except Chaufferie.DoesNotExist:
        #Si l'objet 1 n'existe pas, on l'initialise
        c = Chaufferie.objects.create(user=request.user.username, nbChaudiere=1, nbDivers=0)
        c.save()

    #Initialisation de la liste de points
    try:
        #Si l'objet 1 est existant alors on le récupère
        listePts = Point.objects.filter(user=request.user.username)
    except Point.DoesNotExist:
        #Si l'objet 1 n'existe pas, on ne fait rien
        listePts = Point.objects.create(user=request.user.username)

    ##Déclaration des deux formulaires
    initial_data = c
    nbChaudform = nbChaudForm(request.POST)
    chaudform = chaudForm(request.POST)

    #Détection de l'envoie d'un formulaire
    if request.method == "POST":
        #Choix des actions en fonction du formulaire soumit
        # Soumission du formulaire déterminant le nombre de chaudières
        if (request.POST.get("form_type") == "nbChaudform" and nbChaudform.is_valid()):
            message = "Nommer les libellés si nécessaire, ajuster les points puis exporter en Xls" 
            c.nomInstal = request.POST.get('nomInstal') #Récupération du nombre de chaudières saisies
            c.nbChaudiere = int(request.POST.get('nbChaudiere')) #Récupération du nombre de chaudières saisies
            c.nbDivers = int(request.POST.get('nbDivers')) #Récupération du nombre de chaudières saisies
            c.nbCircReg = int(request.POST.get('nbCircReg')) #Récupération du nombre de circuits régulés saisies
            c.ECSpres = bool(request.POST.get('ECSpres'))
            c.ECSprepa = bool(request.POST.get('ECSprepa'))
            c.modemNec = bool(request.POST.get('modemNec'))
            c.nbPortModem = int(request.POST.get('nbPortModem'))
            c.ecranNec = bool(request.POST.get('ecranNec'))
            
            Chaufferie.creationGeneral(c) #Ajout partie générale dans la base de données
            Chaufferie.creationChaudiere(c) #Ajout des chaudières dans la base de données
            Chaufferie.creationDivers(c) #Ajout des équipements Divers dans la base de données
            Chaufferie.creationCircReg(c) #Ajout des circuits régulés dans la base de données
            Chaufferie.creationECS(c) #Ajout de l'ECS dans la base de données       

            c = Chaufferie.objects.get(user=request.user.username) #Relecture pour affichage
            nbChaudform.save()

        # Soumission du formulaire configuration des équipements
        elif (request.POST.get("form_type") == "chaudform"): #and chaudform.is_valid()):
            c=Chaufferie.objects.get(user=request.user.username) #Relecture pour affichage
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
            if request.POST.get("Supp") !=None:
                print("valeur")
                print(request.POST.get('Supp'))
                Point.objects.filter(pk=int(request.POST.get('Supp'))).delete()
            elif request.POST.get("Add") !=None:
                listePts.create(
                    equip= request.POST.get('Add'),
                    type= 'Add',
                    libelle= 'nouveau libellé', 
                    TM=0, 
                    TS=0, 
                    TR=0, 
                    TC=0,
                    Supp=False,
                    user=request.user.username)
            else:
                message = updateListe(request)

        # Soumission du formulaire de chargement liste de point
        elif (request.POST.get("form_type") == "uploadList"): 
            file = request.FILES['myfile']
            print("chargement d'une liste de point ", file.name)
            upload_file(request, file)
            # return redirect("polls:uploadfile", filename="template_Listedepoints.xlsx", newName="template_Listedepoints.xlsx")

        # Soumission du formulaire de téléchargement liste de point
        elif (request.POST.get("form_type") == "downloadListTemplate"): #and chaudform.is_valid()):
            print("téléchargement")
            return redirect("polls:downloadfile", filename="template_Listedepoints.xlsx", newName="template_Listedepoints.xlsx")

        # Soumission du formulaire de téléchargement liste de point
        elif (request.POST.get("form_type") == "exportExcelList"):
            message = generationXls(request, request.user.username)
            return redirect("polls:downloadfile", filename="listedepoints.xlsx", newName=c.nomInstal)

        # RAZ de la liste de point
        elif (request.POST.get("form_type") == "RAZList"):
            RAZListe(request)
    else:
        nbChaudform = nbChaudForm()

    c = Chaufferie.objects.get(user=request.user.username) #Relecture pour affichage
    listePts = Point.objects.filter(user=request.user.username,).order_by('equip').values()
    calculTotaux(request.user.username)
    return render(request, 'polls/listePts.html', {
        'nbChaudform': nbChaudform, 
        'chaudform': chaudform, 
        'chaufferie': c,
        'listePts': listePts,
        'message': message
        })
    



