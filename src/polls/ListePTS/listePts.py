from ..models.modelsEquip import point, Liste
from ..models.modelsChaudiere import Chaufferie

#Fonction permettant la génération de la liste de points
def generationListe(chaufferie):
    #Déclaration d'un point
    # point.objects.all().delete()
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

    #Ajout de la dernière ligne de la liste TOTAUX
    calculTotaux(liste)

    #Affichage Liste
    for listePts in liste.pts:
        print(listePts.libelle + 
            ' TM:' + str(listePts.TM) + 
            ' TS:' + str(listePts.TS) + 
            ' TR:' + str(listePts.TR) +
            ' TC:' + str(listePts.TC)
            )

#Fonction permettant l'ajout des points chaudières
def ajoutPtsChaud(liste, Chaudieres):
    for chaud in Chaudieres:
        #Défaut pompe
        liste.pts.append(point(
            libelle= chaud.nomChaud + ' Défaut pompe ', 
            TM=0, 
            TS=chaud.nbPpe, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Commande pompe
        liste.pts.append(point(
            libelle= chaud.nomChaud + ' Commande pompe ', 
            TM=0, 
            TS=0, 
            TR=chaud.nbPpe, 
            TC=0
        ))
        liste.save()  

        #Fin de course V2V
        liste.pts.append(point(
            libelle= chaud.nomChaud + ' Fin de course V2V ', 
            TM=0, 
            TS=chaud.nbV2V, 
            TR=0, 
            TC=0
        ))
        liste.save()  

        #Commande V2V
        liste.pts.append(point(
            libelle= chaud.nomChaud + ' Commande V2V ', 
            TM=0, 
            TS=0, 
            TR=0, 
            TC=chaud.nbV2V
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
            libelle= ' TOTAUX (' + str(TotTM+TotTS+TotTR+TotTC) + ' points)', 
            TM=TotTM, 
            TS=TotTS, 
            TR=TotTR, 
            TC=TotTC
        ))