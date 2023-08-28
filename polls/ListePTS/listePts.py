from ..models.Typology.modelsEquip import point, Liste, Temp, SyntDefaut, DefPpe, CmdChaud, CmdPpe, CmdV2V, FdcV2V
from ..models.Typology.modelsEquip import CmdV2V, FdcV2V, Info, Amb, CmdV3V, CmdBal
from ..models.Typology.modelsChaudiere import Chaufferie
from .export import generationXls

#Fonction permettant la génération de la liste de points
def generationListe(request, chaufferie):
    #Déclaration d'un point
    pts = point

    #Initialisation de la liste de points
    try:
        #Si l'objet 1 est existant alors on le récupère
        # liste = Liste.objects.get(user=request.user.username)
        liste = Liste(request.user.username)
        liste.pts.clear()
        #Si la liste est existante on supprime la dermnière ligne des TOTAUX pour les recalculer
        # if len(liste.pts)>0 :
        #     liste.pts.pop()
        
    except Liste.DoesNotExist:
        #Si l'objet 1 n'existe pas, on ne fait rien
        liste = Liste.objects.create(user=request.user.username)

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

    # liste.pts.sort(key=lambda x: x.equip)

    

    # suppPts(liste, chaufferie.General, chaufferie.Chaudieres, chaufferie.Divers, chaufferie.CircReg, chaufferie.ECS)

    #Ajout de la dernière ligne de la liste TOTAUX
    calculTotaux(liste)

    #Création du fichier EXCEL
    message = "Prêt pour la génération du fichier Excel"

    return message

#Fonction de mise à jour liste
def updateListe(listePts, request):
    i = 0
    for liste in listePts.pts:
        if (i != len(listePts.pts) - 1):
                # liste.equip = request.POST.get('nomEquip'+str(i))
                liste.libelle = request.POST.get('libelle'+str(i))
                if (request.POST.get('TM'+str(i)) is not None):
                    liste.TM = int(request.POST.get('TM'+str(i)))
                if (request.POST.get('TS'+str(i)) is not None):
                    liste.TS = int(request.POST.get('TS'+str(i)))
                if (request.POST.get('TR'+str(i)) is not None):
                    liste.TR = int(request.POST.get('TR'+str(i)))
                if (request.POST.get('TC'+str(i)) is not None):
                    liste.TC = int(request.POST.get('TC'+str(i)))  

        i = i +1
    #Ajout de la dernière ligne de la liste TOTAUX
    listePts.pts.pop()
    calculTotaux(listePts)       
    # listePts.save()
    return "Mise à jour liste effectué"

#Fonction permettant la génération de la liste de points
# def geneTempListe(request):
#     #Déclaration d'un point
#     pts = point

#     #Déclaration 
#     c = Chaufferie

#     #Initialisation de la liste de points
#     try:
#         #Si l'objet 1 est existant alors on le récupère
#         liste = Liste.objects.get(user=request.user.username)
#         liste.pts.clear()
#     except Liste.DoesNotExist:
#         #Si l'objet 1 n'existe pas, on ne fait rien
#         liste = Liste.objects.create(user=request.user.username)

#     # Bouclage en fonction du numéro de la chaudière
#     for chaud in c.Chaudieres:
#         Chaufferie.updateChaudiere(
#             c,
#             numero=chaud.num,
#             nomChaud=chaud.nomChaud,
#             nbBruleur=chaud.nbBruleur,
#             nbPpe=chaud.nbPpe,
#             nbV2V=chaud.nbV2V,
#         )
#     # Bouclage en fonction du numéro de l'équipement divers
#     for divers in c.Divers:
#         Chaufferie.updateDivers(
#             c,
#             numero=divers.num,
#             nomDivers=divers.nomDivers,
#             nbTSsup=divers.nbTSsup,
#             nbPpe=divers.nbPpe,
#             nbV2V=divers.nbV2V,
#         )
#     # Bouclage en fonction du numéro du circuit régulé
#     for circ in c.CircReg:
#         Chaufferie.updateCircReg(
#             c,
#             numero=circ.num,
#             nomCirc=circ.nomCirc,
#             nbTemp=circ.nbTemp,
#             nbPpe=circ.nbPpe,
#             nbV3V=circ.nbV3V,
#         )
#     # Bouclage en fonction du numéro du circuit constant
#     for circ in c.CircCst:
#         Chaufferie.updateCircCst(
#             c,
#             numero=circ.num,
#             nomCirc=circ.nomCirc,
#             nbPpe=circ.nbPpe,
#         )
#     # Bouclage en fonction du numéro de l'ECS
#     for ECS in c.ECS:
#         Chaufferie.updateECS(
#             c,
#             nomECS=ECS.nomECS,
#             nbBallon=ECS.nbBallon,
#             nbV3V=ECS.nbV3V,
#             nbTemp=ECS.nbTemp,
#             nbPpe=ECS.nbPpe,
#         )

#     #Ajout des points pompes chaudières
#     ajoutPtsChaud(liste, c.Chaudieres)

#     #Ajout des points Divers
#     # ajoutPtsDivers(liste, c.Divers)

#     #Ajout des points Circuits Constants
#     # ajoutPtsCircCst(liste, c.CircCst)

#     #Ajout des points Circuits Régulés
#     # ajoutPtsCircReg(liste, c.CircReg)

#     #Ajout des points Circuits Régulés
#     # ajoutPtsECS(liste, c.ECS)

#     #Ajout de la dernière ligne de la liste TOTAUX
#     # calculTotaux(liste)

#     #Affichage Liste
#     # for listePts in liste.pts:
#     #     print( listePts.equip +
#     #         listePts.libelle + 
#     #         ' TM:' + str(listePts.TM) + 
#     #         ' TS:' + str(listePts.TS) + 
#     #         ' TR:' + str(listePts.TR) +
#     #         ' TC:' + str(listePts.TC)
#     #         )
    
#     #Création du fichier EXCEL
#     message = generationXls(liste)

#     return message

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
            liste.pts.append(point(
                equip= gen.nomGen,
                type= '',
                libelle= '', 
                TM=0, 
                TS=0, 
                TR=0, 
                TC=0,
                Supp=False
            )) 
            #Température départ primaire
            liste.pts.append(point(
                equip= gen.nomGen,
                type= 'Temp',
                libelle= 'Température extérieure ', 
                TM=1, 
                TS=0, 
                TR=0, 
                TC=0,
                Supp=False
            ))
            # liste.save()  

            #Défaut synthèse
            liste.pts.append(point(
                equip= gen.nomGen,
                type= 'DefMQE',
                libelle= 'Défaut manque d\'eau ', 
                TM=0, 
                TS=1, 
                TR=0, 
                TC=0,
                Supp=False
            ))
            # liste.save() 

#Fonction permettant l'ajout des points chaudières
def ajoutPtsChaud(liste, Chaudieres):
    for chaud in Chaudieres:
        # Détection si l'objet a été ajouté précédemment
        existEquip = False
        for pts in liste.pts:
            if pts.equip == chaud.nomChaud:
                existEquip = True #L'objet existe déjà dans la liste

        liste.pts.append(point(
                equip= chaud.nomChaud,
                type= '',
                libelle= '', 
                TM=0, 
                TS=0, 
                TR=0, 
                TC=0,
                Supp=False
            )) 
        
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not existEquip :   
            #Température XX
            for i in range(chaud.nbTemp):
                pts = Temp(
                    equip = chaud.nomChaud,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                # liste.save()  

            #Défaut synthèse
            for i in range(chaud.nbDef):
                pts = SyntDefaut(
                    equip = chaud.nomChaud,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                # liste.save()  

            #Défaut pompe
            for i in range(chaud.nbPpe):
                pts = DefPpe(
                    equip = chaud.nomChaud,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save() 

            #Commande pompe
            for i in range(chaud.nbPpe):
                pts = CmdPpe(
                    equip = chaud.nomChaud,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save()
            
            #Commande chaudière
            pts = CmdChaud(
                equip = chaud.nomChaud,
                )
            pts.libelle = pts.libelle
            liste.pts.append(pts)
            #liste.save()

            #Fin de course V2V
            for i in range(chaud.nbV2V):
                pts = FdcV2V(
                    equip = chaud.nomChaud,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save()

            #Commande V2V
            for i in range(chaud.nbV2V):
                pts = CmdV2V(
                    equip = chaud.nomChaud,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save()
        else:
            #Ajout Température
            insertPts(liste, nbTotPts=chaud.nbTemp, nomEquip=chaud.nomChaud, type='Temp')
            #Ajout Défaut Pompe
            insertPts(liste, nbTotPts=chaud.nbPpe, nomEquip=chaud.nomChaud, type='DefPpe')
            #Ajout Commande Pompe
            insertPts(liste, nbTotPts=chaud.nbPpe, nomEquip=chaud.nomChaud, type='CmdPpe')
            #Ajout Commande V2V
            insertPts(liste, nbTotPts=chaud.nbV2V, nomEquip=chaud.nomChaud, type='CmdV2V')
            #Ajout Fin de course V2V
            insertPts(liste, nbTotPts=chaud.nbV2V, nomEquip=chaud.nomChaud, type='FdcV2V')

#Fonction permettant la suppression des points
def suppPts(liste, General, Chaudieres, Divers, CirReg, ECS):
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
            print(p.equip)

            liste.pts.remove(p.equip)
            #liste.save()

        i=i+1
    #liste.save()

#Fonction permettant l'ajout des points Divers
def ajoutPtsDivers(liste, Divers):
    for div in Divers:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste.pts:
            if pts.equip == div.nomDivers:
                exist = True #L'objet existe déjà dans la liste

        liste.pts.append(point(
                equip= div.nomDivers,
                type= '',
                libelle= '', 
                TM=0, 
                TS=0, 
                TR=0, 
                TC=0,
                Supp=False
            )) 
                
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :   
            #TéléSignalisation supplémentaire
            for i in range(div.nbTSsup):
                pts = Info(
                    equip = div.nomDivers,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                # liste.save()

            #Défaut pompe
            for i in range(div.nbPpe):
                pts = DefPpe(
                    equip = div.nomDivers,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                # liste.save()

            #Commande pompe
            for i in range(div.nbPpe):
                pts = CmdPpe(
                    equip = div.nomDivers,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                # liste.save()

            #Fin de course V2V
            for i in range(div.nbV2V):       
                pts = FdcV2V(
                    equip = div.nomDivers,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                # liste.save() 

            #Commande V2V
            for i in range(div.nbV2V): 
                pts = CmdV2V(
                    equip = div.nomDivers,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                # liste.save() 
        else:

            #Ajout Défaut Pompe
            insertPts(liste, nbTotPts=div.nbPpe, nomEquip=div.nomDivers, type='DefPpe')
            #Ajout Commande Pompe
            insertPts(liste, nbTotPts=div.nbPpe, nomEquip=div.nomDivers, type='CmdPpe')
            #Ajout Commande V2V
            insertPts(liste, nbTotPts=div.nbV2V, nomEquip=div.nomDivers, type='CmdV2V')
            #Ajout Fin de course V2V
            insertPts(liste, nbTotPts=div.nbV2V, nomEquip=div.nomDivers, type='FdcV2V')
            #Ajout infos supplémentaire
            insertPts(liste, nbTotPts=div.nbTSsup, nomEquip=div.nomDivers, type='Info')

#Fonction permettant l'ajout des points circuits régulés
def ajoutPtsCircReg(liste, CircReg):
    for circ in CircReg:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste.pts:
            if pts.equip == circ.nomCirc:
                exist = True #L'objet existe déjà dans la liste

        liste.pts.append(point(
                equip= circ.nomCirc,
                type= '',
                libelle= '', 
                TM=0, 
                TS=0, 
                TR=0, 
                TC=0,
                Supp=False
            )) 
        
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :   
            #Mesure de température
            for i in range(circ.nbTemp):
                pts = Temp(
                    equip = circ.nomCirc,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save()  

            #Mesure de température Ambiant
            for i in range(circ.nbAmb): 
                pts = Amb(
                    equip = circ.nomCirc,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save()  

            #Défaut pompe
            for i in range(circ.nbPpe):
                pts = DefPpe(
                    equip = circ.nomCirc,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save() 

            #Commande pompe
            for i in range(circ.nbPpe):
                pts = CmdPpe(
                    equip = circ.nomCirc,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save() 

            #Commande V3V
            for i in range(circ.nbV3V):
                pts = CmdV3V(
                    equip = circ.nomCirc,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save() 
        else:
            #Ajout Température
            insertPts(liste, nbTotPts=circ.nbTemp, nomEquip=circ.nomCirc, type='Temp')
            #Ajout Défaut Pompe
            insertPts(liste, nbTotPts=circ.nbPpe, nomEquip=circ.nomCirc, type='DefPpe')
            #Ajout Commande Pompe
            insertPts(liste, nbTotPts=circ.nbPpe, nomEquip=circ.nomCirc, type='CmdPpe')
            #Ajout Commande V3V
            insertPts(liste, nbTotPts=circ.nbV3V, nomEquip=circ.nomCirc, type='CmdV3V')
            #Ajout Température Ambiant
            insertPts(liste, nbTotPts=circ.nbAmb, nomEquip=circ.nomCirc, type='Amb')

#Fonction permettant l'ajout des points Divers
def ajoutPtsECS(liste, ECS):
    for e in ECS:
        # Détection si l'objet a été ajouté précédemment
        exist = False
        for pts in liste.pts:
            if pts.equip == e.nomECS:
                exist = True #L'objet existe déjà dans la liste

        liste.pts.append(point(
                equip= e.nomECS,
                type= '',
                libelle= '', 
                TM=0, 
                TS=0, 
                TR=0, 
                TC=0,
                Supp=False
            )) 
        
        #L'objet n'existe pas donc on l'ajoute dans la liste
        if not exist :          
            #Mesure de température
            for i in range(e.nbTemp):
                pts = Temp(
                    equip = e.nomECS,
                    )
                pts.libelle = 'Température départ/retour'
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save()  

            #Défaut ECS
            for i in range(e.nbDef):
                pts = SyntDefaut(
                    equip = e.nomECS,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save() 

            #Défaut pompe
            for i in range(e.nbPpe):
                pts = DefPpe(
                    equip = e.nomECS,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save() 

            #Commande pompe
            for i in range(e.nbPpe):
                pts = CmdPpe(
                    equip = e.nomECS,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save()

            #Commande V3V
            for i in range(e.nbV3V):
                pts = CmdV3V(
                    equip = e.nomECS,
                    )
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save() 

            #Mesure température ballon
            for i in range(e.nbBallon):
                pts = Temp(
                    equip = e.nomECS,
                    )
                pts.libelle = 'Température ballon '
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save()  

            #Mesure épingle ballon
            for i in range(e.nbBallon):
                pts = CmdBal(
                    equip = e.nomECS,
                    )
                pts.libelle = 'Epingle ballon '
                pts.libelle = pts.libelle + str(i+1)
                liste.pts.append(pts)
                #liste.save() 
        else:
            #Ajout Température
            insertPts(liste, nbTotPts=e.nbTemp, nomEquip=e.nomECS, type='Temp')
            #Ajout Défaut ECS
            insertPts(liste, nbTotPts=e.nbDef, nomEquip=e.nomECS, type='SynthDef')
            #Ajout Défaut Pompe
            insertPts(liste, nbTotPts=e.nbPpe, nomEquip=e.nomECS, type='DefPpe')
            #Ajout Commande Pompe
            insertPts(liste, nbTotPts=e.nbPpe, nomEquip=e.nomECS, type='CmdPpe')
            #Ajout Commande V3V
            insertPts(liste, nbTotPts=e.nbV3V, nomEquip=e.nomECS, type='CmdV3V')
            #Ajout Température Ballon
            insertPts(liste, nbTotPts=e.nbBallon, nomEquip=e.nomECS, type='Temp')
            #Ajout Comande épingle ballon
            insertPts(liste, nbTotPts=e.nbBallon, nomEquip=e.nomECS, type='CmdBal')

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
            TC=TotTC,
            type='',
            Supp=False
        ))

#Fonction insertion points 
def insertPts(liste,nbTotPts, nomEquip, type):
    #Détection du nombre des points à insérer
    y=0
    index_lastType = 0
    for index,pts in enumerate(liste.pts):
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
        liste.pts.insert(index_lastType+1, ptsInsert)
        index_lastType += 1
        valInit += 1

    
