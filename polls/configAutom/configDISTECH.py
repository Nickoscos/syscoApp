from ..models.Typology.modelsEquip import Point
from ..models.Pack.modelsAutom import Automate
from ..models.Pack.modelsAutom import carteAutom
from django.db.models import Q

def configDISTECH(request, username, modemNec, portModem, nbMbus):
    liste = Point.objects.filter(user=username)
    NbUI_Sup = 0
    NbAI_Sup = 0
    NbAO_Sup = 0
    NbDO_Sup = 0
    NbUO_Sup = 0
    # Détection nombre d'entrées/sorties nécessaire
    for point in liste:
        if point.libelle.find("TOTAUX") != -1:
            NbAO = point.TR     # Nombre d'entrées analogiques
            NbDO = point.TC     # Nombre de sorties digitales
            NbDI = point.TS     # Nombre d'entrées digitales
            NbAI = point.TM     # Nombre d'entrées analogiques

    NbRessources = round((NbAO+NbDO+NbDI+NbAI) * 30/100 + (NbAO+NbDO+NbDI+NbAI), 0)

    catalogue = carteAutom.objects.filter(Q(marque='DISTECH') | Q(type= 'MODEM'))

    try:
        Automate.objects.filter(Q(user=request.user.username) & Q(marque="DISTECH") | Q(type='MODEM')).delete()
    except Automate.DoesNotExist:
        print("aucun automate dimensionné")

    if len(liste)>1 :
        #Etape 1 : Ajout de l'alimentation
        carteAajouter = None
        for carte in catalogue:
            if carte.type =="ALIM" and carte.reference.find('PS100-240') != -1:                    
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
            print("Aucune alimentation correspondante trouvée")

        #Etape 2 : Ajout de la CPU dans la configuration
        #On parcoure le catalogue en fonction du type de la carte recherchée
        MinRessources = 9999 
        for carte in catalogue:
            if carte.type =="CPU" and carte.Imagerie == True and carte.ressources > NbRessources:                    
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
        else : 
            print("Aucune CPU correspondante trouvée")
                        

        #Etape 3 : Ajout des cartes de sorties analogiques 
        AO_Autom = NbAO
        NbUO_Sup = 0
        print("nombre de AO au départ : ", AO_Autom )
        while AO_Autom > 0:
            MinReserves = 9999 
            carteAajouter = None
            for carte in catalogue:
                if carte.type =="Carte_ES" and (carte.UO > 0 or carte.DO_UO > 0) and carte.UI >= (NbAI - NbUI_Sup):                    
                    NbAOcarte = (carte.UO + carte.DO_UO)
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
            NbUO_Sup = carteAajouter.UO + carteAajouter.DO_UO # Calcul du nombre de sorties universel
            NbUI_Sup = NbUI_Sup + carteAajouter.UI
            AO_Autom = AO_Autom - NbUO_Sup
            if AO_Autom <= 0 :
                NbUO_Sup = abs(AO_Autom) # Calcul du nombre de sorties universelles non utilisées
                break

        #Etape 4: Ajout des cartes de sorties digitales 
        DO_Autom = NbDO - NbUO_Sup
        NbDO_Sup = 0
        
        print("nombre de DO : ", DO_Autom )
        
        while DO_Autom > 0:
            MinReserves = 9999 
            MinReserves_UO = 9999
            carteAajouter = None
            prixCarteDO =0
            #Détermine la carte de sorties digitales 
            for carte in catalogue:
                if carte.type =="Carte_ES" and (carte.DO > 0 or carte.DO_UO or carte.DOR > 0) :                    
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
            print(DO_Autom)
            if DO_Autom <= 0 :
                NbDO_Sup = abs(DO_Autom) # Calcul du nombre de sorties digitales non utilisées
                break


        # #Etape 4 : Ajout des cartes d'entrées analogiques           
        # AI_Autom = NbAI- NbUI_Sup
        # while AI_Autom > 0:
        #     MinReserves = 9999 
        #     carteAajouter = None

        #     for carte in catalogue:
        #         if carte.type =="Carte_ES" and (carte.UI > 0):                       
        #             NbUIcarte = (carte.UI)
        #             if AI_Autom - NbUIcarte < MinReserves :
        #                 carteAajouter = carte
        #                 AI_Autom -= NbUIcarte #Calcul des ES manquantes
        #                 MinReserves = AI_Autom - NbUIcarte

        #     if carteAajouter != None : 
        #         Automate.objects.create(
        #             type=carteAajouter.type, 
        #             marque=carteAajouter.marque,
        #             reference=carteAajouter.reference,
        #             DI=carteAajouter.DI,
        #             DO=carteAajouter.DO,
        #             AI=carteAajouter.AI,
        #             AO=carteAajouter.AO,
        #             UI=carteAajouter.UI,
        #             UO=carteAajouter.UO,
        #             DOR=carteAajouter.DOR,
        #             DO_UO=carteAajouter.DO_UO,
        #             nbEmpl=carteAajouter.nbEmpl,
        #             extension=carteAajouter.extension,
        #             rs232=carteAajouter.rs232,
        #             rs485=carteAajouter.rs485,
        #             ressources=carteAajouter.ressources,
        #             maxModbus=carteAajouter.maxModbus,
        #             Imagerie=carteAajouter.Imagerie,
        #             maxMbus=carteAajouter.maxMbus,
        #             prix=carteAajouter.prix,
        #             user=request.user.username
        #         )
        #     else : 
        #         print("Aucune carte correspondante trouvée")
        #         break

        #     #Détermination des entrées universelles en SPARE pour une utilisation en tant que sorties digitales
        #     AI_Autom = AI_Autom - NbUI_Sup

        #     if AI_Autom <= 0 :
        #         if AI_Autom<0:
        #             NbUI_Sup = abs(AI_Autom) # Calcul du nombre de sorties universelles non utilisées
        #         else :
        #             NbUI_Sup = 0
        #         break          


        # # Etape 3 : Ajout des cartes de sorties digitales 
        
        
        # #Etape 5 : Ajout des cartes d'entrées digitales           
        # DI_Autom = NbDI - NbUI_Sup
        
        # while DI_Autom > 0:
        #     MinPrixMoy_ES = 9999 
            
        #     for carte in catalogue:
        #         if carte.type =="Carte_ES" and (carte.DI > 0 or carte.UI > 0):
        #             #Détermination du prix moyen d'une entrée/sortie avec la carte retenue
        #             PrixMoy_ES = carte.prix / (carte.DI + carte.DO + carte.AI + carte.AO 
        #                                     + carte.UI + carte.UO + carte.DOR + carte.DO_UO)
                    
        #             if MinPrixMoy_ES > PrixMoy_ES :
        #                 carteAajouter = carte
        #                 DI_Autom -= (carte.DI + carte.UI) #Calcul des ES manquantes
        #                 MinPrixMoy_ES = PrixMoy_ES

        #     if carteAajouter != None : 
        #         Automate.objects.create(
        #             type=carteAajouter.type, 
        #             marque=carteAajouter.marque,
        #             reference=carteAajouter.reference,
        #             DI=carteAajouter.DI,
        #             DO=carteAajouter.DO,
        #             AI=carteAajouter.AI,
        #             AO=carteAajouter.AO,
        #             UI=carteAajouter.UI,
        #             UO=carteAajouter.UO,
        #             DOR=carteAajouter.DOR,
        #             DO_UO=carteAajouter.DO_UO,
        #             nbEmpl=carteAajouter.nbEmpl,
        #             extension=carteAajouter.extension,
        #             rs232=carteAajouter.rs232,
        #             rs485=carteAajouter.rs485,
        #             ressources=carteAajouter.ressources,
        #             maxModbus=carteAajouter.maxModbus,
        #             Imagerie=carteAajouter.Imagerie,
        #             maxMbus=carteAajouter.maxMbus,
        #             prix=carteAajouter.prix,
        #             user=request.user.username
        #         )
        #     else : 
        #         print("Aucune carte correspondante trouvée")
        #         break           

        # #Etape 6: Ajout de la carte Mbus 
        # NbEquipMbus = nbMbus
        # while NbEquipMbus > 0:
        #     NbMbusMspare = 9999 
        #     for carte in catalogue:
        #         if carte.type =="COM" and carte.maxMbus > 0:
        #             if NbMbusMspare > carte.maxMbus - NbEquipMbus and (carte.maxMbus - NbEquipMbus) > 0:
        #                 NbMbusMspare = carte.maxMbus - NbEquipMbus #Calcul des equipements manquants       
        #                 carteAajouter = carte
                        

        #     if carteAajouter != None : 
        #         Automate.objects.create(
        #             type=carteAajouter.type, 
        #             marque=carteAajouter.marque,
        #             reference=carteAajouter.reference,
        #             DI=carteAajouter.DI,
        #             DO=carteAajouter.DO,
        #             AI=carteAajouter.AI,
        #             AO=carteAajouter.AO,
        #             UI=carteAajouter.UI,
        #             UO=carteAajouter.UO,
        #             DOR=carteAajouter.DOR,
        #             DO_UO=carteAajouter.DO_UO,
        #             nbEmpl=carteAajouter.nbEmpl,
        #             extension=carteAajouter.extension,
        #             rs232=carteAajouter.rs232,
        #             rs485=carteAajouter.rs485,
        #             ressources=carteAajouter.ressources,
        #             maxModbus=carteAajouter.maxModbus,
        #             Imagerie=carteAajouter.Imagerie,
        #             maxMbus=carteAajouter.maxMbus,
        #             prix=carteAajouter.prix,
        #             user=request.user.username
        #         )
        #         NbEquipMbus -= carteAajouter.maxMbus 
        #     else : 
        #         print("Aucune carte correspondante trouvée")
        #         break

        # #Etape 7: Ajout du modem
        # if modemNec == True:
        #     for carte in catalogue:
        #         if carte.type == "MODEM" and carte.reference.find('Routeur') != -1 and carte.reference.find(str(portModem) + " ports") != -1 :
        #             print("test")
        #             Automate.objects.create(
        #                 type=carte.type, 
        #                 marque=carte.marque,
        #                 reference=carte.reference,
        #                 DI=carte.DI,
        #                 DO=carte.DO,
        #                 AI=carte.AI,
        #                 AO=carte.AO,
        #                 UI=carte.UI,
        #                 UO=carte.UO,
        #                 DOR=carte.DOR,
        #                 DO_UO=carte.DO_UO,
        #                 nbEmpl=carte.nbEmpl,
        #                 extension=carte.extension,
        #                 rs232=carte.rs232,
        #                 rs485=carte.rs485,
        #                 ressources=carte.ressources,
        #                 maxModbus=carte.maxModbus,
        #                 Imagerie=carte.Imagerie,
        #                 maxMbus=carte.maxMbus,
        #                 prix=carte.prix,
        #                 user=request.user.username
        #             )
        #         if carte.type =="MODEM" and carte.reference.find('Routeur') !=-1 and carte.reference.find("APWR000058") != -1 :
        #             Automate.objects.create(
        #                 type=carte.type, 
        #                 marque=carte.marque,
        #                 reference=carte.reference,
        #                 DI=carte.DI,
        #                 DO=carte.DO,
        #                 AI=carte.AI,
        #                 AO=carte.AO,
        #                 UI=carte.UI,
        #                 UO=carte.UO,
        #                 DOR=carte.DOR,
        #                 DO_UO=carte.DO_UO,
        #                 nbEmpl=carte.nbEmpl,
        #                 extension=carte.extension,
        #                 rs232=carte.rs232,
        #                 rs485=carte.rs485,
        #                 ressources=carte.ressources,
        #                 maxModbus=carte.maxModbus,
        #                 Imagerie=carte.Imagerie,
        #                 maxMbus=carte.maxMbus,
        #                 prix=carte.prix,
        #                 user=request.user.username
        #             )
            
                    

        #Etape finale : Affichage de la configuration
        automate = Automate.objects.filter(Q(user=username) & (Q(marque="DISTECH") | Q(type="MODEM")))
        prixAutomate = 0
        for carte in automate:
            print("Type : ", carte.type, ", Marque : ", carte.marque, ", Référence : ", carte.reference, ", Prix : ", carte.prix ,"€")
            prixAutomate += carte.prix

        print("Coût total configuration automate: ", prixAutomate, "€")

    
    