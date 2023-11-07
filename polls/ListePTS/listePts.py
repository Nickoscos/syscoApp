from ..models.Typology.modelsEquip import Point, Temp, SyntDefaut, DefPpe, CmdChaud, CmdPpe, CmdV2V, FdcV2V
from ..models.Typology.modelsEquip import CmdV2V, FdcV2V, Info, Amb, CmdV3V, CmdBal, CptMbus, CptModbus
from ..models.Typology.modelsChaudiere import Chaufferie
from .export import generationXls
from django.shortcuts import redirect, render

#Fonction permettant la génération de la liste de points
def generationListe(request, chaufferie):
    try:
        Point.objects.filter(user=request.user.username).delete()
        liste = Point.objects.filter(user=request.user.username)
    except Point.DoesNotExist:
        liste = Point.objects.create(user=request.user.username)

    # #Ajout des points Général
    ajoutPtsGeneral(chaufferie.General, request.user.username)

    # #Ajout des points chaudières
    ajoutPtsChaud(chaufferie.Chaudieres, request.user.username)

    # #Ajout des points Divers
    ajoutPtsDivers(chaufferie.Divers, request.user.username)

    # #Ajout des points Circuits Régulés
    ajoutPtsCircReg(chaufferie.CircReg, request.user.username)

    # #Ajout des points Circuits Régulés
    ajoutPtsECS(chaufferie.ECS, request.user.username)

    # #Ajout des compteurs
    ajoutPtsCpt(chaufferie, request.user.username)

    # suppPts(chaufferie.General, chaufferie.Chaudieres, chaufferie.Divers, chaufferie.CircReg, chaufferie.ECS, request.user.username)

    # #Ajout de la dernière ligne de la liste TOTAUX
    calculTotaux(request.user.username)




#Fonction de mise à jour liste
def updateListe(request):
    listePts = Point.objects.filter(user=request.user.username)
    i = 0
    for pts in listePts:
        if (i != len(listePts) - 1):
                # liste.equip = request.POST.get('nomEquip'+str(i))
                pts.libelle = request.POST.get('libelle'+str(pts.id))
                if (request.POST.get('TM'+str(pts.id)) is not None):
                    pts.TM = int(request.POST.get('TM'+str(pts.id)))
                if (request.POST.get('TS'+str(pts.id)) is not None):
                    pts.TS = int(request.POST.get('TS'+str(pts.id)))
                if (request.POST.get('TR'+str(pts.id)) is not None):
                    pts.TR = int(request.POST.get('TR'+str(pts.id)))
                if (request.POST.get('TC'+str(pts.id)) is not None):
                    pts.TC = int(request.POST.get('TC'+str(pts.id))) 
                if (request.POST.get('Mbus'+str(pts.id)) is not None):
                    pts.Mbus = int(request.POST.get('Mbus'+str(pts.id))) 
                if (request.POST.get('Modbus'+str(pts.id)) is not None):
                    pts.Modbus = int(request.POST.get('Modbus'+str(pts.id))) 
                pts.save()
        i = i +1
    #Ajout de la dernière ligne de la liste TOTAUX 
    calculTotaux(request.user.username)      
    
    return "Mise à jour liste effectué"


#Fonction permettant l'ajout des points généraux
def ajoutPtsGeneral(General, username):
    liste = Point.objects.filter(user=username)
    # Détection si l'objet a été ajouté précédemment
    exist = False
    for pts in liste:
        if pts.equip == General[0].nomGen:
            exist = True #L'objet existe déjà dans la liste
    #L'objet n'existe pas donc on l'ajoute dans la liste
    if not exist :               
        for gen in General:
            #Température départ primaire
            liste.create(
                equip= gen.nomGen,
                type= 'Temp',
                libelle= 'Température extérieure ', 
                TM=1, 
                TS=0, 
                TR=0, 
                TC=0,
                Mbus=0,
                Modbus=0,
                Supp=False,
                user=username)

            #Défaut synthèse
            liste.create(
                equip= gen.nomGen,
                type= 'DefMQE',
                libelle= 'Défaut manque d\'eau ', 
                TM=0, 
                TS=1, 
                TR=0, 
                TC=0,
                Mbus=0,
                Modbus=0,
                Supp=False,
                user=username
            )
    
    
#Fonction permettant l'ajout des points chaudières
def ajoutPtsChaud(Chaudieres, username):
    liste = Point.objects.filter(user=username)
    for chaud in Chaudieres:
        # Détection si l'objet a été ajouté précédemment
        existEquip = False
        for pts in liste:
            if pts.equip == chaud.nomChaud:
                existEquip = True #L'objet existe déjà dans la liste
        
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not existEquip :   
            #Température XX
            for i in range(chaud.nbTemp):
                pts = Temp(
                    equip = chaud.nomChaud,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Défaut synthèse
            for i in range(chaud.nbDef):
                pts = SyntDefaut(
                    equip = chaud.nomChaud,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Défaut pompe
            for i in range(chaud.nbPpe):
                pts = DefPpe(
                    equip = chaud.nomChaud,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Commande pompe
            for i in range(chaud.nbPpe):
                pts = CmdPpe(
                    equip = chaud.nomChaud,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)
            
            #Commande chaudière
            pts = CmdChaud(
                equip = chaud.nomChaud,
                username= username
                )
            pts.libelle = pts.libelle
            liste.create(equip= pts.equip,
                type= pts.type,
                libelle= pts.libelle, 
                TM=pts.TM, 
                TS=pts.TS, 
                TR=pts.TR, 
                TC=pts.TC,
                Mbus=pts.Mbus,
                Modbus=pts.Modbus,
                Supp=pts.Supp,
                user=pts.username)

            #Fin de course V2V
            for i in range(chaud.nbV2V):
                pts = FdcV2V(
                    equip = chaud.nomChaud,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Commande V2V
            for i in range(chaud.nbV2V):
                pts = CmdV2V(
                    equip = chaud.nomChaud,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)


#Fonction permettant l'ajout des compteurs
def ajoutPtsCpt(chaufferie, username):
    liste = Point.objects.filter(user=username)
   
    # Ajout des compteurs MBus
    for c in range(chaufferie.nbMbus):
        pts = CptMbus(
            equip = "Compteurs",
            username= username
            )
        pts.libelle = "Compteur Mbus " + str(c+1)
        liste.create(equip= pts.equip,
            type= pts.type,
            libelle= pts.libelle, 
            TM=0, 
            TS=0, 
            TR=0, 
            TC=0,
            Mbus=pts.Mbus,
            Modbus=pts.Modbus,
            Supp=pts.Supp,
            user=pts.username)
        
    # Ajout des compteurs ModBus
    for c in range(chaufferie.nbModbus):
        pts = CptModbus(
            equip = "Compteurs",
            username= username
            )
        pts.libelle = "Compteur Modbus " + str(c+1)
        liste.create(equip= pts.equip,
            type= pts.type,
            libelle= pts.libelle, 
            TM=0, 
            TS=0, 
            TR=0, 
            TC=0,
            Mbus=pts.Mbus,
            Modbus=pts.Modbus,
            Supp=pts.Supp,
            user=pts.username)
        
    # Ajout des compteurs Impulsionnels
    for c in range(chaufferie.nbImp):
        pts = Info(
            equip = "Compteurs",
            username= username
            )
        pts.libelle = "Compteur Impulsionnel " + str(c+1)
        liste.create(equip= pts.equip,
            type= pts.type,
            libelle= pts.libelle, 
            TM=0, 
            TS=1, 
            TR=0, 
            TC=0,
            Mbus=0,
            Modbus=0,
            Supp=pts.Supp,
            user=pts.username)

            
#Fonction permettant l'ajout des points Divers
def ajoutPtsDivers(Divers, username):
    liste = Point.objects.filter(user=username)
    for div in Divers:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste:
            if pts.equip == div.nomDivers:
                exist = True #L'objet existe déjà dans la liste
                
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :   
            #TéléSignalisation supplémentaire
            for i in range(div.nbTSsup):
                pts = Info(
                    equip = div.nomDivers,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Défaut pompe
            for i in range(div.nbPpe):
                pts = DefPpe(
                    equip = div.nomDivers,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Commande pompe
            for i in range(div.nbPpe):
                pts = CmdPpe(
                    equip = div.nomDivers,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Fin de course V2V
            for i in range(div.nbV2V):       
                pts = FdcV2V(
                    equip = div.nomDivers,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Commande V2V
            for i in range(div.nbV2V): 
                pts = CmdV2V(
                    equip = div.nomDivers,
                    username= username
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

#Fonction permettant l'ajout des points circuits régulés
def ajoutPtsCircReg(CircReg, username):
    liste = Point.objects.filter(user=username)
    for circ in CircReg:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste:
            if pts.equip == circ.nomCirc:
                exist = True #L'objet existe déjà dans la liste
        
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :   
            #Mesure de température
            for i in range(circ.nbTemp):
                pts = Temp(
                    equip = circ.nomCirc,
                    username= username
                    )
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Mesure de température Ambiant
            for i in range(circ.nbAmb): 
                pts = Amb(
                    equip = circ.nomCirc,
                    username= username
                    )
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Défaut pompe
            for i in range(circ.nbPpe):
                pts = DefPpe(
                    equip = circ.nomCirc,
                    username= username
                    )
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Commande pompe
            for i in range(circ.nbPpe):
                pts = CmdPpe(
                    equip = circ.nomCirc,
                    username= username
                    )
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Commande V3V
            for i in range(circ.nbV3V):
                pts = CmdV3V(
                    equip = circ.nomCirc,
                    username= username
                    )
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)


#Fonction permettant l'ajout des points Divers
def ajoutPtsECS(ECS, username):
    liste = Point.objects.filter(user=username)
    for e in ECS:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste:
            if pts.equip == e.nomECS:
                exist = True #L'objet existe déjà dans la liste
        
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :          
            #Mesure de température
            for i in range(e.nbTemp):
                pts = Temp(
                    equip = e.nomECS,
                    username= username
                    )
                pts.libelle = 'Température départ/retour'
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Défaut ECS
            for i in range(e.nbDef):
                pts = SyntDefaut(
                    equip = e.nomECS,
                    username= username
                    )
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Défaut pompe
            for i in range(e.nbPpe):
                pts = DefPpe(
                    equip = e.nomECS,
                    username= username
                    )
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Commande pompe
            for i in range(e.nbPpe):
                pts = CmdPpe(
                    equip = e.nomECS,
                    username= username
                    )
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Commande V3V
            for i in range(e.nbV3V):
                pts = CmdV3V(
                    equip = e.nomECS,
                    username= username
                    )
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)

            #Mesure température ballon
            for i in range(e.nbBallon):
                pts = Temp(
                    equip = e.nomECS,
                    username= username
                    )
                pts.libelle = 'Température ballon '
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)  

            #Mesure épingle ballon
            for i in range(e.nbBallon):
                pts = CmdBal(
                    equip = e.nomECS,
                    username= username
                    )
                pts.libelle = 'Epingle ballon '
                pts.libelle = pts.libelle + " " + str(i+1)
                liste.create(equip= pts.equip,
                    type= pts.type,
                    libelle= pts.libelle, 
                    TM=pts.TM, 
                    TS=pts.TS, 
                    TR=pts.TR, 
                    TC=pts.TC,
                    Mbus=pts.Mbus,
                    Modbus=pts.Modbus,
                    Supp=pts.Supp,
                    user=pts.username)
    

#Calcul des totaux par type d'entrées/sorties
def calculTotaux(username):
    Point.objects.filter(user=username, type='TOTAL').delete()
    liste = Point.objects.filter(user=username)
    #Initialisation des totaux
    TotTM = 0
    TotTS = 0
    TotTR = 0
    TotTC = 0
    TotMbus = 0
    TotModbus = 0
    
    #Calcul de la somme des points par type
    for Pts in liste:
        
        TotTM =  TotTM + Pts.TM
        TotTS =  TotTS + Pts.TS
        TotTR =  TotTR + Pts.TR
        TotTC =  TotTC + Pts.TC
        TotMbus =  TotMbus + Pts.Mbus
        TotModbus =  TotModbus + Pts.Modbus

    liste.create(
                equip= 'zzzzeTOTAL', #zzzz ajouté pour permettre d'afficher le point en dernière ligne de la liste sur la page
                type= 'TOTAL',
                libelle= 'TOTAUX (' + str(TotTM+TotTS+TotTR+TotTC+TotMbus+TotModbus) + ' points)', 
                TM=TotTM, 
                TS=TotTS, 
                TR=TotTR, 
                TC=TotTC,
                Mbus=TotMbus,
                Modbus=TotModbus,
                Supp=False,
                user=username
            )

#Fonction insertion points 
def insertPts(liste,nbTotPts, nomEquip, type):
    #Détection du nombre des points à insérer
    y=0
    index_lastType = 0
    for index,pts in enumerate(liste):
        if pts.equip == nomEquip and pts.type==type and y<=nbTotPts:
            y=y+1
            index_lastType = index

    ajoutNb = nbTotPts - y
    valInit = y

    #Insertion dans le fichier en faisant un regroupement par type
    for i in range(ajoutNb):
        #Détection du type de point à insérer
        if type == 'Temp':
            ptsInsert = Temp(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)
        elif type == 'DefPpe':
            ptsInsert = DefPpe(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)
        elif type == 'CmdPpe':
            ptsInsert = CmdPpe(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)
        elif type == 'CmdV2V':
            ptsInsert = CmdV2V(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)   
        elif type == 'FdcV2V':
            ptsInsert = FdcV2V(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)           
        elif type == 'Info':
            ptsInsert = Info(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)    
        elif type == 'Amb':
            ptsInsert = Amb(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)   
        elif type == 'CmdV3V':
            ptsInsert = CmdV3V(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)   
        elif type == 'CmdBal':
            ptsInsert = CmdV3V(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)  
        elif type == 'SynthDef':
            ptsInsert = SyntDefaut(
                equip = nomEquip,
                )
            ptsInsert.libelle = ptsInsert.libelle + str(valInit+1)  
        #Insertion
        liste.insert(index_lastType+1, ptsInsert)
        index_lastType += 1
        valInit += 1
    liste.save()

#Fonction permettant d'effacer la liste de points
def RAZListe(request):
    try:
        Point.objects.filter(user=request.user.username).delete()
    except Point.DoesNotExist:
        print("Liste vide")
