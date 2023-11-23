from ..models.Typology.modelsEquip import Point
from ..models.Pack.modelsAutom import Automate
from ..models.Pack.modelsAutom import carteAutom

def configWIT(request, username, modemNec, nbMbus):
    liste = Point.objects.filter(user=username)
    NbUI_Sup = 0
    NbAI_Sup = 0
    NbDI_Sup = 0
    NbAO_Sup = 0
    # Détection nombre d'entrées/sorties nécessaire
    for point in liste:
        if point.libelle.find("TOTAUX") != -1:
            NbAO = point.TR     # Nombre d'entrées analogiques
            NbDO = point.TC     # Nombre de sorties digitales
            NbDI = point.TS     # Nombre d'entrées digitales
            NbAI = point.TM     # Nombre d'entrées analogiques

    NbRessources = round((NbAO+NbDO+NbDI+NbAI) * 30/100 + (NbAO+NbDO+NbDI+NbAI), 0)

    catalogue = carteAutom.objects.filter(marque='WIT')

    try:
        Automate.objects.filter(user=request.user.username, marque="WIT").delete()
    except Automate.DoesNotExist:
        print("aucun automate dimensionné")

    if len(liste)>1 :
        #Etape 1 : Ajout de la CPU dans la configuration
        #On parcoure le catalogue en fonction du type de la carte recherchée
        for carte in catalogue:
            if modemNec == True:
                if carte.type =="CPU" and carte.reference.find('4G') != -1 and carte.reference.find('4G') != -1 and carte.reference.find('PROCESS') != -1:
                    Automate.objects.create(
                        type=carte.type,
                        marque=carte.marque, 
                        reference=carte.reference,
                        DI=carte.DI,
                        DO=carte.DO,
                        AI=carte.AI,
                        AO=carte.AO,
                        UI=carte.UI,
                        UO=carte.UO,
                        DOR=carte.DOR,
                        DO_UO=carte.DO_UO,
                        nbEmpl=carte.nbEmpl,
                        extension=carte.extension,
                        rs232=carte.rs232,
                        rs485=carte.rs485,
                        ressources=carte.ressources,
                        maxModbus=carte.maxModbus,
                        Imagerie=carte.Imagerie,
                        maxMbus=carte.maxMbus,
                        prix=carte.prix,
                        user=request.user.username
                    )

            else:
                if carte.type =="CPU" and carte.reference.find('4G') == -1 and carte.reference.find('PROCESS') != -1:
                    Automate.objects.create(
                        type=carte.type, 
                        marque=carte.marque, 
                        reference=carte.reference,
                        DI=carte.DI,
                        DO=carte.DO,
                        AI=carte.AI,
                        AO=carte.AO,
                        UI=carte.UI,
                        UO=carte.UO,
                        DOR=carte.DOR,
                        DO_UO=carte.DO_UO,
                        nbEmpl=carte.nbEmpl,
                        extension=carte.extension,
                        rs232=carte.rs232,
                        rs485=carte.rs485,
                        ressources=carte.ressources,
                        maxModbus=carte.maxModbus,
                        Imagerie=carte.Imagerie,
                        maxMbus=carte.maxMbus,
                        prix=carte.prix,
                        user=request.user.username
                    )

        #Etape 2 : Ajout des cartes de sorties analogiques 
        AO_Autom = NbAO
        NbUO_Sup = 0
        
        while AO_Autom > 0:
            MinReserves = 9999 
            carteAajouter = None
            for carte in catalogue:
                if carte.type =="Carte_ES" and (carte.AO > 0 or carte.UO > 0 or carte.DO_UO > 0):                    
                    NbAOcarte = (carte.AO + carte.UO + carte.DO_UO)
                    if AO_Autom - NbAOcarte < MinReserves :
                        carteAajouter = carte
                        MinReserves = AO_Autom - NbAOcarte

            if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
                    marque=carteAajouter.marque, 
                    reference=carteAajouter.reference,
                    DI=carteAajouter.DI,
                    DO=carteAajouter.DO,
                    AI=carteAajouter.AI,
                    AO=carteAajouter.AO,
                    UI=carteAajouter.UI,
                    UO=carteAajouter.UO,
                    DOR=carteAajouter.DOR,
                    DO_UO=carteAajouter.DO_UO,
                    nbEmpl=carteAajouter.nbEmpl,
                    extension=carteAajouter.extension,
                    rs232=carteAajouter.rs232,
                    rs485=carteAajouter.rs485,
                    ressources=carteAajouter.ressources,
                    maxModbus=carteAajouter.maxModbus,
                    Imagerie=carteAajouter.Imagerie,
                    maxMbus=carteAajouter.maxMbus,
                    prix=carteAajouter.prix,
                    user=request.user.username
                )
            else : 
                print("Aucune carte correspondante trouvée")
                break

            #Détermination des sorties universelles en SPARE pour une utilisation en tant que sorties digitales
            NbUO_Sup = NbUO_Sup + carteAajouter.UO + carteAajouter.DO_UO  # Calcul du nombre de sorties universel
            NbUI_Sup = NbUI_Sup + carteAajouter.UI
            NbAI_Sup = NbAI_Sup + carteAajouter.AI
            NbAO_Sup = carteAajouter.AO
            AO_Autom = AO_Autom - carteAajouter.AO - carteAajouter.UO - carteAajouter.DO_UO
            if AO_Autom <= 0 :
                break

        NbAO_Sup = abs(AO_Autom) # Calcul du nombre de sorties universelles non utilisées
        
        # Etape 3 : Ajout des cartes de sorties digitales 
        DO_Autom = NbDO - NbUO_Sup
        NbDO_Sup = 0


        while DO_Autom > 0:
            MinReserves = 9999 
            MinReserves_UO = 9999
            carteAajouter = None
            prixCarteDO =0
            for carte in catalogue:
                if carte.type =="Carte_ES" and (carte.DO > 0 or carte.DOR > 0 or carte.DO_UO > 0):
                    NbDOcarte = (carte.DO_UO + carte.DO + carte.DOR)
                    if (DO_Autom - NbDOcarte) < MinReserves :
                        carteAajouter = carte
                        MinReserves_UO = MinReserves #Mémorise le nombre de sorties manquantes avant l'ajout de la carte 
                        MinReserves = DO_Autom - NbDOcarte
                        prixCarteDO = carte.prix

            #On Vérifie si une carte de sortie universelles ne serait pas moins couteuse 
            if MinReserves <= 0: # Toutes les cartes ont été dimensionnées
                for carte in catalogue:
                    if carte.type =="Carte_ES" and (carte.UO > 0 or carte.DO_UO > 0) :                    
                        NbDOcarte = (carte.DO_UO + carte.UO)
                        if (DO_Autom - NbDOcarte) < MinReserves_UO: # une carte UO pour remplacer la dernière ne serait-elle pas 
                            if carte.prix<=prixCarteDO :    # moins chère
                                carteAajouter = carte
                            MinReserves_UO = DO_Autom - NbDOcarte

            if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
                    marque=carteAajouter.marque,
                    reference=carteAajouter.reference,
                    DI=carteAajouter.DI,
                    DO=carteAajouter.DO,
                    AI=carteAajouter.AI,
                    AO=carteAajouter.AO,
                    UI=carteAajouter.UI,
                    UO=carteAajouter.UO,
                    DOR=carteAajouter.DOR,
                    DO_UO=carteAajouter.DO_UO,
                    nbEmpl=carteAajouter.nbEmpl,
                    extension=carteAajouter.extension,
                    rs232=carteAajouter.rs232,
                    rs485=carteAajouter.rs485,
                    ressources=carteAajouter.ressources,
                    maxModbus=carteAajouter.maxModbus,
                    Imagerie=carteAajouter.Imagerie,
                    maxMbus=carteAajouter.maxMbus,
                    prix=carteAajouter.prix,
                    user=request.user.username
                )
            else : 
                print("Aucune carte correspondante trouvée")
                break

            #Détermination des sorties universelles en SPARE
            NbDO_Sup = carteAajouter.DO + carteAajouter.DO_UO + carteAajouter.DOR + carteAajouter.UO # Calcul du nombre de sorties universe
            DO_Autom = DO_Autom - NbDO_Sup
            if DO_Autom <= 0 :
                break
        
        NbDO_Sup = abs(DO_Autom) # Calcul du nombre de sorties digitales non utilisées
        

        # Etape 4 : Ajout des cartes d'entrées analogiques           
        AI_Autom = NbAI- NbUI_Sup - NbAI_Sup
        while AI_Autom > 0:
            MinReserves = 9999 
            carteAajouter = None
            for carte in catalogue:
                if carte.type =="Carte_ES" and (carte.AI > 0 or carte.UI > 0):                    
                    NbAIcarte = (carte.AI + carte.UI)
                    if AI_Autom - NbAIcarte < MinReserves :
                        carteAajouter = carte
                        MinReserves = AI_Autom - NbAIcarte

            if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
                    marque=carteAajouter.marque,
                    reference=carteAajouter.reference,
                    DI=carteAajouter.DI,
                    DO=carteAajouter.DO,
                    AI=carteAajouter.AI,
                    AO=carteAajouter.AO,
                    UI=carteAajouter.UI,
                    UO=carteAajouter.UO,
                    DOR=carteAajouter.DOR,
                    DO_UO=carteAajouter.DO_UO,
                    nbEmpl=carteAajouter.nbEmpl,
                    extension=carteAajouter.extension,
                    rs232=carteAajouter.rs232,
                    rs485=carteAajouter.rs485,
                    ressources=carteAajouter.ressources,
                    maxModbus=carteAajouter.maxModbus,
                    Imagerie=carteAajouter.Imagerie,
                    maxMbus=carteAajouter.maxMbus,
                    prix=carteAajouter.prix,
                    user=request.user.username
                )
            else : 
                print("Aucune carte correspondante trouvée")
                break

            #Détermination des entrées universelles en SPARE pour une utilisation en tant que sorties digitales
            NbAI_Sup = NbAI_Sup + carteAajouter.AI
            AI_Autom = AI_Autom - NbAI_Sup
            if AI_Autom <= 0 :
                break 

        NbUI_Sup = abs(AI_Autom) # Calcul du nombre de sorties universelles non utilisées          

        # #Etape 5 : Ajout des cartes d'entrées digitales           
        DI_Autom = NbDI - NbUI_Sup - NbDI_Sup
        NbDI_Sup = 0
        NbUI_Sup = 0
        while DI_Autom > 0:
            MinReserves = 9999 
            carteAajouter = None
            prixCarteDI =0
            for carte in catalogue:
                if carte.type =="Carte_ES" and (carte.DI > 0 ) :                    
                    NbDIcarte = (carte.DI)
                    if (DI_Autom - NbDIcarte) < MinReserves :
                        carteAajouter = carte
                        MinReserves = DI_Autom - NbDIcarte
                        prixCarteDI = carte.prix

            #On Vérifie si une carte de sortie universelles ne serait pas moins couteuse 
            if MinReserves <= 0: # Toutes les cartes ont été dimensionnées
                for carte in catalogue:
                    if carte.type =="Carte_ES" and (carte.UI > 0) :                    
                        NbDIcarte = (carte.UI)
                        if (DI_Autom - NbDIcarte) < MinReserves_DI: # une carte UO pour remplacer la dernière ne serait-elle pas 
                            if carte.prix<=prixCarteDI :    # moins chère
                                carteAajouter = carte
                            MinReserves_DI = DI_Autom - NbDIcarte

            if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
                    marque=carteAajouter.marque,
                    reference=carteAajouter.reference,
                    DI=carteAajouter.DI,
                    DO=carteAajouter.DO,
                    AI=carteAajouter.AI,
                    AO=carteAajouter.AO,
                    UI=carteAajouter.UI,
                    UO=carteAajouter.UO,
                    DOR=carteAajouter.DOR,
                    DO_UO=carteAajouter.DO_UO,
                    nbEmpl=carteAajouter.nbEmpl,
                    extension=carteAajouter.extension,
                    rs232=carteAajouter.rs232,
                    rs485=carteAajouter.rs485,
                    ressources=carteAajouter.ressources,
                    maxModbus=carteAajouter.maxModbus,
                    Imagerie=carteAajouter.Imagerie,
                    maxMbus=carteAajouter.maxMbus,
                    prix=carteAajouter.prix,
                    user=request.user.username
                )
            else : 
                print("Aucune carte correspondante trouvée")
                break     

            #Détermination des sorties universelles en SPARE
            NbDI_Sup = carteAajouter.DI + carteAajouter.UI # Calcul du nombre de sorties universe
            DI_Autom = DI_Autom - NbDI_Sup
            if DI_Autom <= 0 :
                break      

        #Etape 6: Ajout de l'Add-on interface web
        for carte in catalogue:
                if carte.type =="CPU" and carte.reference.find('Intravision') != -1:
                    carteAajouter = carte
                    break
        
        if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
                    marque=carteAajouter.marque,
                    reference=carteAajouter.reference,
                    DI=0,
                    DO=0,
                    AI=0,
                    AO=0,
                    UI=0,
                    UO=0,
                    DOR=0,
                    DO_UO=0,
                    nbEmpl=0,
                    extension=False,
                    rs232=0,
                    rs485=0,
                    ressources=0,
                    maxModbus=0,
                    Imagerie=False,
                    maxMbus=0,
                    prix=carteAajouter.prix,
                    user=request.user.username
                )

        #Etape 7: Ajout de la carte Mbus 
        NbEquipMbus = nbMbus
        while NbEquipMbus > 0:
            NbMbusMspare = 9999 
            for carte in catalogue:
                if carte.type =="COM" and carte.maxMbus > 0:
                    if NbMbusMspare > carte.maxMbus - NbEquipMbus and (carte.maxMbus - NbEquipMbus) > 0:
                        NbMbusMspare = carte.maxMbus - NbEquipMbus #Calcul des equipements manquants       
                        carteAajouter = carte
                        

            if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
                    marque=carteAajouter.marque,
                    reference=carteAajouter.reference,
                    DI=carteAajouter.DI,
                    DO=carteAajouter.DO,
                    AI=carteAajouter.AI,
                    AO=carteAajouter.AO,
                    UI=carteAajouter.UI,
                    UO=carteAajouter.UO,
                    DOR=carteAajouter.DOR,
                    DO_UO=carteAajouter.DO_UO,
                    nbEmpl=carteAajouter.nbEmpl,
                    extension=carteAajouter.extension,
                    rs232=carteAajouter.rs232,
                    rs485=carteAajouter.rs485,
                    ressources=carteAajouter.ressources,
                    maxModbus=carteAajouter.maxModbus,
                    Imagerie=carteAajouter.Imagerie,
                    maxMbus=carteAajouter.maxMbus,
                    prix=carteAajouter.prix,
                    user=request.user.username
                )
                NbEquipMbus -= carteAajouter.maxMbus 
            else : 
                print("Aucune carte correspondante trouvée")
                break

        #Etape 8: Ajout de l'embase principale
        automate = Automate.objects.filter(user=username, marque="WIT")
        NbCarteES = 0
        NbCarteCOM = 0

        for carte in automate:
            if carte.type.find('Carte_ES') != -1:
                NbCarteES += 1
            elif carte.type.find('COM') != -1:
                NbCarteCOM += 1

        NbCarte = NbCarteES + NbCarteCOM

        # Ajout de l'embase de base
        for carte in catalogue:
                if carte.type =="EMBASE" and carte.extension == False and carte.reference.find('PLUG310') != -1:
                    NbCarte -= carte.nbEmpl
                    carteAajouter = carte
        
        if carteAajouter != None : 
            Automate.objects.create(
                type=carteAajouter.type, 
                marque=carteAajouter.marque,
                reference=carteAajouter.reference,
                DI=carteAajouter.DI,
                DO=carteAajouter.DO,
                AI=carteAajouter.AI,
                AO=carteAajouter.AO,
                UI=carteAajouter.UI,
                UO=carteAajouter.UO,
                DOR=carteAajouter.DOR,
                DO_UO=carteAajouter.DO_UO,
                nbEmpl=carteAajouter.nbEmpl,
                extension=carteAajouter.extension,
                rs232=carteAajouter.rs232,
                rs485=carteAajouter.rs485,
                ressources=carteAajouter.ressources,
                maxModbus=carteAajouter.maxModbus,
                Imagerie=carteAajouter.Imagerie,
                maxMbus=carteAajouter.maxMbus,
                prix=carteAajouter.prix,
                user=request.user.username
            )
        else : 
            print("Aucune embase correspondante trouvée")

        while NbCarte > 0:
            NbEmplspare = 9999
            for carte in catalogue:
                if carte.type =="EMBASE" and carte.extension == True and carte.nbEmpl > 0 and NbEmplspare > carte.nbEmpl - NbCarte:
                    NbEmplspare = carte.nbEmpl - NbCarte #Calcul des emplacements manquants       
                    carteAajouter = carte

            if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
                    marque=carteAajouter.marque,
                    reference=carteAajouter.reference,
                    DI=carteAajouter.DI,
                    DO=carteAajouter.DO,
                    AI=carteAajouter.AI,
                    AO=carteAajouter.AO,
                    UI=carteAajouter.UI,
                    UO=carteAajouter.UO,
                    DOR=carteAajouter.DOR,
                    DO_UO=carteAajouter.DO_UO,
                    nbEmpl=carteAajouter.nbEmpl,
                    extension=carteAajouter.extension,
                    rs232=carteAajouter.rs232,
                    rs485=carteAajouter.rs485,
                    ressources=carteAajouter.ressources,
                    maxModbus=carteAajouter.maxModbus,
                    Imagerie=carteAajouter.Imagerie,
                    maxMbus=carteAajouter.maxMbus,
                    prix=carteAajouter.prix,
                    user=request.user.username
                )
                NbCarte -= carteAajouter.nbEmpl 
            else : 
                print("Aucune embase correspondante trouvée")
                break

        #Etape 9: Ajout des upgrade ressources
        #On parcoure le catalogue en fonction du type de la carte recherchée
        if NbRessources > 100:
            MinRessources = 9999 
            carteAajouter = None
            for carte in catalogue:
                if carte.type =="CPU" and carte.ressources > NbRessources:                    
                    #Détermination du prix moyen d'une entrée/sortie avec la carte retenue
                    if MinRessources > carte.ressources :
                        carteAajouter = carte
                        MinRessources = carte.ressources
                
            if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
                    marque=carteAajouter.marque,
                    reference=carteAajouter.reference,
                    DI=carteAajouter.DI,
                    DO=carteAajouter.DO,
                    AI=carteAajouter.AI,
                    AO=carteAajouter.AO,
                    UI=carteAajouter.UI,
                    UO=carteAajouter.UO,
                    DOR=carteAajouter.DOR,
                    DO_UO=carteAajouter.DO_UO,
                    nbEmpl=carteAajouter.nbEmpl,
                    extension=carteAajouter.extension,
                    rs232=carteAajouter.rs232,
                    rs485=carteAajouter.rs485,
                    ressources=carteAajouter.ressources,
                    maxModbus=carteAajouter.maxModbus,
                    Imagerie=carteAajouter.Imagerie,
                    maxMbus=carteAajouter.maxMbus,
                    prix=carteAajouter.prix,
                    user=request.user.username
                )

        #Etape finale : Affichage de la configuration
        automate = Automate.objects.filter(user=username, marque="WIT")
        prixAutomate = 0
        for carte in automate:
            print("Type : ", carte.type, ", Marque : ", carte.marque, ", Référence : ", carte.reference, ", Prix : ", carte.prix ,"€")
            prixAutomate += carte.prix
        print("Coût total configuration automate: ", prixAutomate, "€")

    
    