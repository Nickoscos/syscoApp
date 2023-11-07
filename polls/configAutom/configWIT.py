from ..models.Typology.modelsEquip import Point
from ..models.Pack.modelsAutom import Automate
from ..models.Pack.modelsAutom import carteAutom

def configWIT(request, username, modemNec, nbMbus):
    liste = Point.objects.filter(user=username)
    NbUI_Sup = 0
    NbAI_Sup = 0
    # Détection nombre d'entrées/sorties nécessaire
    for point in liste:
        if point.libelle.find("TOTAUX") != -1:
            NbAO = point.TR     # Nombre d'entrées analogiques
            NbDO = point.TC     # Nombre de sorties digitales
            NbDI = point.TS     # Nombre d'entrées digitales
            NbAI = point.TM     # Nombre d'entrées analogiques

    catalogue = carteAutom.objects.all()
    print("config automate")

    try:
        Automate.objects.filter(user=request.user.username).delete()
    except Automate.DoesNotExist:
        print("aucun automate dimensionné")

    if len(liste)>1 :
        #Etape 1 : Ajout de la CPU dans la configuration
        #On parcoure le catalogue en fonction du type de la carte recherchée
        for carte in catalogue:
            if modemNec == True:
                if carte.type =="CPU" and carte.reference.find('4G') != -1 and carte.reference.find('PROCESS') != -1:
                    Automate.objects.create(
                        type=carte.type, 
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
            MinPrixMoy_ES = 9999 
            for carte in catalogue:
                if carte.type =="Carte_ES" and (carte.AO > 0 or carte.UO > 0 or carte.DO_UO > 0):
                    AO_Autom -= (carte.AO + carte.UO + carte.DO_UO) #Calcul des ES manquantes
                    
                    #Détermination du prix moyen d'une entrée/sortie avec la carte retenue
                    PrixMoy_ES = carte.prix / (carte.DI + carte.DO + carte.AI + carte.AO 
                                               + carte.UI + carte.UO + carte.DOR + carte.DO_UO)
                    if MinPrixMoy_ES > PrixMoy_ES :
                        carteAajouter = carte

            if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
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

                #Détermination des entrées en SPARE pour une utilisation
                NbUI_Sup = NbUI_Sup + carteAajouter.UI  # Mémorisation du nombre d'entrées universelles de la carte ajoutée
                NbAI_Sup = NbAI_Sup + carteAajouter.AI  # Mémorisation du nombre d'entrées universelles de la carte ajoutée
            else : 
                print("Aucune carte correspondante trouvée")
                break

            #Détermination des sorties universelles en SPARE pour une utilisation en tant que sorties digitales
            if carteAajouter.UO > 0 or carteAajouter.DO_UO > 0:
                NbUO_Sup = carteAajouter.UO + carteAajouter.DO_UO # Calcul du nombre de sorties universelles
            if AO_Autom <= 0 :
                if NbUO_Sup > AO_Autom:
                    NbUO_Sup = AO_Autom # Calcul du nombre de sorties universelles non utilisées
                else :
                    NbUO_Sup = 0
                break

        # Etape 3 : Ajout des cartes de sorties digitales 
        DO_Autom = NbDO - NbUO_Sup
        NbDO_Sup = 0
        while DO_Autom > 0:
            MinPrixMoy_ES = 9999 
            for carte in catalogue:
                if carte.type =="Carte_ES" and (carte.DO > 0 or carte.UO > 0 or carte.DOR > 0 or carte.DO_UO > 0):
                    DO_Autom -= (carte.DO + carte.UO + carte.DOR + carte.DO_UO) #Calcul des ES manquantes

                    #Détermination du prix moyen d'une entrée/sortie avec la carte retenue
                    PrixMoy_ES = carte.prix / (carte.DI + carte.DO + carte.AI + carte.AO 
                                               + carte.UI + carte.UO + carte.DOR + carte.DO_UO)
                    if MinPrixMoy_ES > PrixMoy_ES :
                        carteAajouter = carte

            if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
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
                #Détermination des entrées en SPARE pour une utilisation
                NbUI_Sup = NbUI_Sup + carteAajouter.UI  # Mémorisation du nombre d'entrées universelles de la carte ajoutée
                NbAI_Sup = NbAI_Sup + carteAajouter.AI  # Mémorisation du nombre d'entrées universelles de la carte ajoutée
            else : 
                print("Aucune carte correspondante trouvée")
                break

            #Détermination des sorties universelles en SPARE
            if carte.UO > 0 or carte.DO_UO > 0:
                NbUO_Sup = carte.UO + carte.DO_UO # Calcul du nombre de sorties universelles
            if DO_Autom <= 0 :
                if NbUO_Sup > DO_Autom:
                    NbUO_Sup = DO_Autom # Calcul du nombre de sorties universelles non utilisées
                else :
                    NbUO_Sup = 0
                break
        

        #Etape 4 : Ajout des cartes d'entrées analogiques           
        AI_Autom = NbAI
        if AI_Autom > (NbAI_Sup + NbUI_Sup):
            while AI_Autom > 0:
                MinPrixMoy_ES = 9999 
                
                for carte in catalogue:
                    if carte.type =="Carte_ES" and (carte.AI > 0 or carte.UI > 0):
                        AI_Autom -= (carte.AI + carte.UI) #Calcul des ES manquantes
                        
                        #Détermination du prix moyen d'une entrée/sortie avec la carte retenue
                        PrixMoy_ES = carte.prix / (carte.DI + carte.DO + carte.AI + carte.AO 
                                                + carte.UI + carte.UO + carte.DOR + carte.DO_UO)
                        
                        if MinPrixMoy_ES > PrixMoy_ES :
                            carteAajouter = carte

                if carteAajouter != None : 
                    Automate.objects.create(
                        type=carteAajouter.type, 
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
                if carteAajouter.UI >= 0 or carteAajouter.DI >= 0:
                    NbDI_Sup = carteAajouter.UI + carteAajouter.DI # Calcul du nombre de sorties universelles
                if AI_Autom <= 0 :
                    if NbUI_Sup > AI_Autom:
                        NbUI_Sup = AI_Autom + NbDI_Sup # Calcul du nombre de sorties universelles non utilisées
                    else :
                        NbUI_Sup = 0 + NbDI_Sup
                else:
                    NbUI_Sup = NbUI_Sup + NbAI_Sup - AI_Autom             

        #Etape 5: Ajout de l'Add-on interface web
        for carte in catalogue:
                if carte.type =="CPU" and carte.reference.find('Intravision') != -1:
                    carteAajouter = carte
                    break
        
        if carteAajouter != None : 
                Automate.objects.create(
                    type=carteAajouter.type, 
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

        #Etape 6: Ajout de la carte Mbus 
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

        #Etape 7: Ajout de l'embase principale
        automate = Automate.objects.filter(user=username)
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

        #Etape finale : Affichage de la configuration
        automate = Automate.objects.filter(user=username)
        prixAutomate = 0
        for carte in automate:
            print("Type : ", carte.type, ", Référence : ", carte.reference, ", Prix : ", carte.prix ,"€")
            prixAutomate += carte.prix
        print("Coût total configuration automate: ", prixAutomate, "€")

    
    