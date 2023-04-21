from ..models.Typology.modelsEquip import point, Liste
from ..models.Typology.modelsChaudiere import Chaufferie
from .export import generationXls

#Fonction permettant la génération de la liste de points
def generationListe(chaufferie):
    #Déclaration d'un point
    pts = point

    #Initialisation de la liste de points
    try:
        #Si l'objet 1 est existant alors on le récupère
        liste = Liste.objects.get(id=1)
        #Si la liste est existante on supprime la dermnière ligne des TOTAUX pour les recalculer
        if len(liste.pts)>0 :
            liste.pts.pop()
        # liste.pts.clear()
    except Liste.DoesNotExist:
        #Si l'objet 1 n'existe pas, on ne fait rien
        liste = Liste.objects.create(id=1)

    #Ajout des points Général
    ajoutPtsGeneral(liste, chaufferie.General)

    #Ajout des points chaudières
    ajoutPtsChaud(liste, chaufferie.Chaudieres)

    #Ajout des points Divers
    ajoutPtsDivers(liste, chaufferie.Divers)

    #Ajout des points Circuits Régulés
    ajoutPtsCircReg(liste, chaufferie.CircReg)

    #Ajout des points Circuits Régulés
    ajoutPtsECS(liste, chaufferie.ECS)

    suppPtsChaud(liste, chaufferie.General, chaufferie.Chaudieres, chaufferie.Divers, chaufferie.CircReg, chaufferie.ECS)

    #Ajout de la dernière ligne de la liste TOTAUX
    calculTotaux(liste)

    #Affichage Liste
    for listePts in liste.pts:
        print( listePts.equip +
            listePts.libelle + 
            ' TM:' + str(listePts.TM) + 
            ' TS:' + str(listePts.TS) + 
            ' TR:' + str(listePts.TR) +
            ' TC:' + str(listePts.TC)
            )
    
    #Création du fichier EXCEL
    # message = generationXls(liste)
    message = "Prêt pour la génération du fichier Excel"

    return message

#Fonction de mise à jour liste
def updateListe(listePts, request):
    i = 0
    for liste in listePts.pts:
        if (i != len(listePts.pts) - 1):
                liste.equip = request.POST.get('nomEquip'+str(i))
                liste.libelle = request.POST.get('libelle'+str(i))
                liste.TM = int(request.POST.get('TM'+str(i)))
                liste.TS = int(request.POST.get('TS'+str(i)))
                liste.TR = int(request.POST.get('TR'+str(i)))
                liste.TC = int(request.POST.get('TC'+str(i)))  

        # if (liste.TM == 0 and liste.TS == 0 and liste.TR == 0 and liste.TC == 0):
        #         listePts.pts.remove(liste)

        i = i +1
    #Ajout de la dernière ligne de la liste TOTAUX
    listePts.pts.pop()
    calculTotaux(listePts)       
    listePts.save()
    return "Mise à jour liste effectué"

#Fonction permettant la génération de la liste de points
def geneTempListe():
    #Déclaration d'un point
    pts = point

    #Déclaration 
    c = Chaufferie

    #Initialisation de la liste de points
    try:
        #Si l'objet 1 est existant alors on le récupère
        liste = Liste.objects.get(id=1)
        liste.pts.clear()
    except Liste.DoesNotExist:
        #Si l'objet 1 n'existe pas, on ne fait rien
        liste = Liste.objects.create(id=1)

    # Bouclage en fonction du numéro de la chaudière
    for chaud in c.Chaudieres:
        Chaufferie.updateChaudiere(
            c,
            numero=chaud.num,
            nomChaud=chaud.nomChaud,
            nbBruleur=chaud.nbBruleur,
            nbPpe=chaud.nbPpe,
            nbV2V=chaud.nbV2V,
        )
    # Bouclage en fonction du numéro de l'équipement divers
    for divers in c.Divers:
        Chaufferie.updateDivers(
            c,
            numero=divers.num,
            nomDivers=divers.nomDivers,
            nbTSsup=divers.nbTSsup,
            nbPpe=divers.nbPpe,
            nbV2V=divers.nbV2V,
        )
    # Bouclage en fonction du numéro du circuit régulé
    for circ in c.CircReg:
        Chaufferie.updateCircReg(
            c,
            numero=circ.num,
            nomCirc=circ.nomCirc,
            nbTemp=circ.nbTemp,
            nbPpe=circ.nbPpe,
            nbV3V=circ.nbV3V,
        )
    # Bouclage en fonction du numéro du circuit constant
    for circ in c.CircCst:
        Chaufferie.updateCircCst(
            c,
            numero=circ.num,
            nomCirc=circ.nomCirc,
            nbPpe=circ.nbPpe,
        )
    # Bouclage en fonction du numéro de l'ECS
    for ECS in c.ECS:
        Chaufferie.updateECS(
            c,
            nomECS=ECS.nomECS,
            nbBallon=ECS.nbBallon,
            nbV3V=ECS.nbV3V,
            nbTemp=ECS.nbTemp,
            nbPpe=ECS.nbPpe,
        )

    #Ajout des points pompes chaudières
    ajoutPtsChaud(liste, c.Chaudieres)

    #Ajout des points Divers
    # ajoutPtsDivers(liste, chaufferie.Divers)

    #Ajout des points Circuits Constants
    # ajoutPtsCircCst(liste, chaufferie.CircCst)

    #Ajout des points Circuits Régulés
    # ajoutPtsCircReg(liste, chaufferie.CircReg)

    #Ajout des points Circuits Régulés
    # ajoutPtsECS(liste, chaufferie.ECS)

    #Ajout de la dernière ligne de la liste TOTAUX
    # calculTotaux(liste)

    #Affichage Liste
    for listePts in liste.pts:
        print( listePts.equip +
            listePts.libelle + 
            ' TM:' + str(listePts.TM) + 
            ' TS:' + str(listePts.TS) + 
            ' TR:' + str(listePts.TR) +
            ' TC:' + str(listePts.TC)
            )
    
    #Création du fichier EXCEL
    message = generationXls(liste)

    return message

#Fonction permettant l'ajout des points généraux
def ajoutPtsGeneral(liste, General):
    # Détection si l'objet a été ajouté précédemment
    exist = False
    for pts in liste.pts:
        if pts.equip == General[0].nomGen:
            exist = True #L'objet existe déjà dans la liste
    #L'objet n'existe pas donc on l'ajoute dans la liste
    if not exist :         
        for gen in General:
                #Température départ primaire
                liste.pts.append(point(
                    equip= gen.nomGen,
                    libelle= 'Température extérieure ', 
                    TM=1, 
                    TS=0, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

                #Défaut synthèse
                liste.pts.append(point(
                    equip= gen.nomGen,
                    libelle= 'Défaut manque d\'eau ', 
                    TM=0, 
                    TS=1, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save() 

#Fonction permettant l'ajout des points chaudières
def ajoutPtsChaud(liste, Chaudieres):
    for chaud in Chaudieres:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste.pts:
            if pts.equip == chaud.nomChaud:
                exist = True #L'objet existe déjà dans la liste
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :   
            #Température XX
            for i in range(chaud.nbTemp):
                liste.pts.append(point(
                    equip= chaud.nomChaud,
                    libelle= 'Température ' + str(i+1), 
                    TM=1, 
                    TS=0, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Défaut synthèse
            for i in range(chaud.nbDef):
                liste.pts.append(point(
                    equip= chaud.nomChaud,
                    libelle= 'Synthèse défaut ' + str(i+1), 
                    TM=0, 
                    TS=1, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save() 

            #Défaut pompe
            for i in range(chaud.nbPpe):
                liste.pts.append(point(
                    equip= chaud.nomChaud,
                    libelle= 'Défaut pompe '+ str(i+1), 
                    TM=0, 
                    TS=1, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Commande pompe
            for i in range(chaud.nbPpe):
                liste.pts.append(point(
                    equip= chaud.nomChaud,
                    libelle= 'Commande pompe + Chaudière '+ str(i+1), 
                    TM=0, 
                    TS=0, 
                    TR=0, 
                    TC=1,
                    Supp=False
                ))
                liste.save()  

            #Fin de course V2V
            for i in range(chaud.nbV2V):
                liste.pts.append(point(
                    equip= chaud.nomChaud,
                    libelle= 'Fin de course V2V '+ str(i+1), 
                    TM=0, 
                    TS=1, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Commande V2V
            for i in range(chaud.nbV2V):
                liste.pts.append(point(
                    equip= chaud.nomChaud,
                    libelle= 'Commande V2V '+ str(i+1), 
                    TM=0, 
                    TS=0, 
                    TR=0, 
                    TC=1,
                    Supp=False
                ))
                liste.save()  

#Fonction permettant la suppression des points chaudières
def suppPtsChaud(liste, General, Chaudieres, Divers, CirReg, ECS):
    i=0
    for p in reversed(liste.pts):
        exist = False

        for g in General:
            if p.equip == g.nomGen:
                exist = True
                break

        if not exist:
            for c in Chaudieres:
                if p.equip == c.nomChaud:
                    exist = True
                    break

        if not exist:
            for d in Divers:
                if p.equip == d.nomDivers:
                    exist = True
                    break

        if not exist:
            for cr in CirReg:
                if p.equip == cr.nomCirc:
                    exist = True
                    break
        
        if not exist:
            for e in ECS:
                if p.equip == e.nomECS:
                    exist = True
                    break

        if not exist:
            liste.pts.remove(p)
        # liste.save()
        i=i+1
    liste.save()

#Fonction permettant l'ajout des points Divers
def ajoutPtsDivers(liste, Divers):
    for div in Divers:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste.pts:
            if pts.equip == div.nomDivers:
                exist = True #L'objet existe déjà dans la liste
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :   
            #TéléSignalisation supplémentaire
            for i in range(div.nbTSsup):
                liste.pts.append(point(
                    equip= div.nomDivers,
                    libelle= 'Information supplémentaire '+ str(i+1), 
                    TM=0, 
                    TS=1, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Défaut pompe
            for i in range(div.nbPpe):
                liste.pts.append(point(
                    equip= div.nomDivers,
                    libelle= 'Défaut pompe '+ str(i+1), 
                    TM=0, 
                    TS=1, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Commande pompe
            for i in range(div.nbPpe):
                liste.pts.append(point(
                    equip= div.nomDivers,
                    libelle= 'Commande pompe '+ str(i+1), 
                    TM=0, 
                    TS=0, 
                    TR=1, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Fin de course V2V
            for i in range(div.nbV2V):       
                liste.pts.append(point(
                    equip= div.nomDivers,
                    libelle= 'Fin de course V2V '+ str(i+1), 
                    TM=0, 
                    TS=1, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Commande V2V
            for i in range(div.nbV2V): 
                liste.pts.append(point(
                    equip= div.nomDivers,
                    libelle= 'Commande V2V '+ str(i+1), 
                    TM=0, 
                    TS=0, 
                    TR=0, 
                    TC=1,
                    Supp=False
                ))
                liste.save()  

#Fonction permettant l'ajout des points circuits régulés
def ajoutPtsCircReg(liste, CircReg):
    for circ in CircReg:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste.pts:
            if pts.equip == circ.nomCirc:
                exist = True #L'objet existe déjà dans la liste
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :   
            #Mesure de température
            for i in range(circ.nbTemp): 
                liste.pts.append(point(
                    equip= circ.nomCirc,
                    libelle= 'Température départ '+ str(i+1), 
                    TM=circ.nbTemp, 
                    TS=0, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Mesure de température Ambiant
            for i in range(circ.nbAmb): 
                liste.pts.append(point(
                    equip= circ.nomCirc,
                    libelle= 'Température Ambiant '+ str(i+1), 
                    TM=circ.nbAmb, 
                    TS=0, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Défaut pompe
            for i in range(circ.nbPpe):
                liste.pts.append(point(
                    equip= circ.nomCirc,
                    libelle= 'Défaut pompe '+ str(i+1), 
                    TM=0, 
                    TS=1, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Commande pompe
            for i in range(circ.nbPpe):
                liste.pts.append(point(
                    equip= circ.nomCirc,
                    libelle= 'Commande pompe '+ str(i+1), 
                    TM=0, 
                    TS=0, 
                    TR=1, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Commande V3V
            for i in range(circ.nbV3V):
                liste.pts.append(point(
                    equip= circ.nomCirc,
                    libelle= 'Commande V3V '+ str(i+1), 
                    TM=0, 
                    TS=0, 
                    TR=1, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

#Fonction permettant l'ajout des points Divers
def ajoutPtsECS(liste, ECS):
    for e in ECS:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste.pts:
            if pts.equip == e.nomECS:
                exist = True #L'objet existe déjà dans la liste
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :          
            #Mesure de température
            for i in range(e.nbTemp):
                liste.pts.append(point(
                    equip= e.nomECS,
                    libelle= 'Température départ/retour '+ str(i+1), 
                    TM=1, 
                    TS=0, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Défaut pompe
            for i in range(e.nbPpe):
                liste.pts.append(point(
                    equip= e.nomECS,
                    libelle= 'Défaut pompe '+ str(i+1), 
                    TM=0, 
                    TS=1, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Commande pompe
            for i in range(e.nbPpe):
                liste.pts.append(point(
                    equip= e.nomECS,
                    libelle= 'Commande pompe '+ str(i+1), 
                    TM=0, 
                    TS=0, 
                    TR=1, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Commande V3V
            for i in range(e.nbV3V):
                liste.pts.append(point(
                    equip= e.nomECS,
                    libelle= 'Commande V3V '+ str(i+1), 
                    TM=0, 
                    TS=0, 
                    TR=1, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Mesure température ballon
            for i in range(e.nbBallon):
                liste.pts.append(point(
                    equip= e.nomECS,
                    libelle= 'Température ballon '+ str(i+1), 
                    TM=1, 
                    TS=0, 
                    TR=0, 
                    TC=0,
                    Supp=False
                ))
                liste.save()  

            #Mesure épingle ballon
            for i in range(e.nbBallon):
                liste.pts.append(point(
                    equip= e.nomECS,
                    libelle= 'Epingle ballon '+ str(i+1), 
                    TM=0, 
                    TS=0, 
                    TR=0, 
                    TC=1,
                    Supp=False
                ))
                liste.save() 

#Calcul des totaux par type d'entrées/sorties
def calculTotaux(liste):
    #Initialisation des totaux
    TotTM = 0
    TotTS = 0
    TotTR = 0
    TotTC = 0

    #Calcul de la somme des points par type
    for listPts in liste.pts:
        TotTM =  TotTM + listPts.TM
        TotTS =  TotTS + listPts.TS
        TotTR =  TotTR + listPts.TR
        TotTC =  TotTC + listPts.TC

    liste.pts.append(point(
            equip = '',
            libelle= ' TOTAUX (' + str(TotTM+TotTS+TotTR+TotTC) + ' points)', 
            TM=TotTM, 
            TS=TotTS, 
            TR=TotTR, 
            TC=TotTC
        ))

