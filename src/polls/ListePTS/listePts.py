from ..models.modelsEquip import point, Liste
from ..models.modelsChaudiere import Chaufferie
from .export import generationXls

#Fonction permettant la génération de la liste de points
def generationListe(chaufferie):
    #Déclaration d'un point
    pts = point

    #Initialisation de la liste de points
    try:
        #Si l'objet 1 est existant alors on le récupère
        liste = Liste.objects.get(id=1)
        liste.pts.clear()
    except Liste.DoesNotExist:
        #Si l'objet 1 n'existe pas, on ne fait rien
        liste = Liste.objects.create(id=1)

    #Ajout des points pompes chaudières
    ajoutPtsChaud(liste, chaufferie.Chaudieres)

    #Ajout des points Divers
    ajoutPtsDivers(liste, chaufferie.Divers)

    #Ajout des points Circuits Constants
    ajoutPtsCircCst(liste, chaufferie.CircCst)

    #Ajout des points Circuits Régulés
    ajoutPtsCircReg(liste, chaufferie.CircReg)

    #Ajout des points Circuits Régulés
    ajoutPtsECS(liste, chaufferie.ECS)

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
    message = generationXls(liste)

    return message

#Fonction permettant l'ajout des points chaudières
def ajoutPtsChaud(liste, Chaudieres):
    for chaud in Chaudieres:
        #Défaut pompe
        liste.pts.append(point(
            equip= chaud.nomChaud,
            libelle= ' Défaut pompe ', 
            TM=0, 
            TS=chaud.nbPpe, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Commande pompe
        liste.pts.append(point(
            equip= chaud.nomChaud,
            libelle= 'Commande pompe ', 
            TM=0, 
            TS=0, 
            TR=chaud.nbPpe, 
            TC=0
        ))
        liste.save()  

        #Fin de course V2V
        liste.pts.append(point(
            equip= chaud.nomChaud,
            libelle= 'Fin de course V2V ', 
            TM=0, 
            TS=chaud.nbV2V, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Commande V2V
        liste.pts.append(point(
            equip= chaud.nomChaud,
            libelle= 'Commande V2V ', 
            TM=0, 
            TS=0, 
            TR=0, 
            TC=chaud.nbV2V
        ))
        liste.save()  

#Fonction permettant l'ajout des points Divers
def ajoutPtsDivers(liste, Divers):
    for div in Divers:
        #TéléSignalisation supplémentaire
        liste.pts.append(point(
            equip= div.nomDivers,
            libelle= 'Information supplémentaire ', 
            TM=0, 
            TS=div.nbTSsup, 
            TR=0, 
            TC=0
        ))

        liste.save()  
        #Défaut pompe
        liste.pts.append(point(
            equip= div.nomDivers,
            libelle= 'Défaut pompe ', 
            TM=0, 
            TS=div.nbPpe, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Commande pompe
        liste.pts.append(point(
            equip= div.nomDivers,
            libelle= 'Commande pompe ', 
            TM=0, 
            TS=0, 
            TR=div.nbPpe, 
            TC=0
        ))
        liste.save()  

        #Fin de course V2V
        liste.pts.append(point(
            equip= div.nomDivers,
            libelle= 'Fin de course V2V ', 
            TM=0, 
            TS=div.nbV2V, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Commande V2V
        liste.pts.append(point(
            equip= div.nomDivers,
            libelle= 'Commande V2V ', 
            TM=0, 
            TS=0, 
            TR=0, 
            TC=div.nbV2V
        ))
        liste.save()  

#Fonction permettant l'ajout des points circuits régulés
def ajoutPtsCircReg(liste, CircReg):
    for circ in CircReg:
        #Mesure de température
        liste.pts.append(point(
            equip= circ.nomCirc,
            libelle= 'Température départ ', 
            TM=circ.nbTemp, 
            TS=0, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Défaut pompe
        liste.pts.append(point(
            equip= circ.nomCirc,
            libelle= 'Défaut pompe ', 
            TM=0, 
            TS=circ.nbPpe, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Commande pompe
        liste.pts.append(point(
            equip= circ.nomCirc,
            libelle= 'Commande pompe ', 
            TM=0, 
            TS=0, 
            TR=circ.nbPpe, 
            TC=0
        ))
        liste.save()  

        #Commande V3V
        liste.pts.append(point(
            equip= circ.nomCirc,
            libelle= 'Commande V3V ', 
            TM=0, 
            TS=0, 
            TR=circ.nbV3V, 
            TC=0
        ))
        liste.save()  

#Fonction permettant l'ajout des points circuits constants
def ajoutPtsCircCst(liste, CircCst):
    for circ in CircCst:
        #Défaut pompe
        liste.pts.append(point(
            equip= circ.nomCirc,
            libelle= 'Défaut pompe ', 
            TM=0, 
            TS=circ.nbPpe, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Commande pompe
        liste.pts.append(point(
            equip= circ.nomCirc,
            libelle= 'Commande pompe ', 
            TM=0, 
            TS=0, 
            TR=circ.nbPpe, 
            TC=0
        ))
        liste.save()  

#Fonction permettant l'ajout des points Divers
def ajoutPtsECS(liste, ECS):
    for e in ECS:
        #Mesure de température
        liste.pts.append(point(
            equip= e.nomECS,
            libelle= 'Température départ/retour ', 
            TM=e.nbTemp, 
            TS=0, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Défaut pompe
        liste.pts.append(point(
            equip= e.nomECS,
            libelle= 'Défaut pompe ', 
            TM=0, 
            TS=e.nbPpe, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Commande pompe
        liste.pts.append(point(
            equip= e.nomECS,
            libelle= 'Commande pompe ', 
            TM=0, 
            TS=0, 
            TR=e.nbPpe, 
            TC=0
        ))
        liste.save()  

        #Commande V3V
        liste.pts.append(point(
            equip= e.nomECS,
            libelle= 'Commande V3V ', 
            TM=0, 
            TS=0, 
            TR=e.nbV3V, 
            TC=0
        ))
        liste.save()  

        #Mesure température ballon
        liste.pts.append(point(
            equip= e.nomECS,
            libelle= 'Température ballon ', 
            TM=e.nbBallon, 
            TS=0, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Mesure épingle ballon
        liste.pts.append(point(
            equip= e.nomECS,
            libelle= 'Epingle ballon ', 
            TM=0, 
            TS=0, 
            TR=0, 
            TC=e.nbBallon
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
