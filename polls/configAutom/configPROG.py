from ..models.Typology.modelsEquip import Point
from ..models.Pack.modelsAutom import Prestation

def configPROG(request, username):
    liste = Point.objects.filter(user=username)

    try:
        Prestation.objects.filter(user=request.user.username).delete()
    except Prestation.DoesNotExist:
        print("aucun automate dimensionné")

    # Coefficient par points 
    CoefAI = 15.00/60
    CoefDI = 05.60/60
    CoefAO = 15.00/60
    CoefDO = 05.60/60
    THO = 63.00

    # Détection nombre d'entrées/sorties nécessaire
    for point in liste:
        if point.libelle.find("TOTAUX") != -1:
            NbAO = point.TR     # Nombre d'entrées analogiques
            NbDO = point.TC     # Nombre de sorties digitales
            NbDI = point.TS     # Nombre d'entrées digitales
            NbAI = point.TM     # Nombre d'entrées analogiques

    # Calcul prestation par type d'ES
    HeureAI = round(CoefAI*NbAI)
    HeureDI = round(CoefDI*NbDI)
    HeureAO = round(CoefAO*NbAO)
    HeureDO = round(CoefDO*NbDO)

    # Calcul cout Analyse Fonctionnelle
    if (NbAO + NbAI + NbDO + NbDI) >= 60 :
        coutAF = 8 * THO
    else :
        coutAF = 4 * THO
    
    # Calcul cout programmation
    coutProg = round((HeureAI + HeureDI + HeureAO + HeureDO), 2) * THO

    # Calcul cout IHM
    coutIHM = round(0.15 * (NbAO + NbAI + NbDO + NbDI), 2) * THO

    # Calcul Mise En Service
    if (NbAO + NbAI + NbDO + NbDI) >= 64 :
        coutMES = round(16 * THO, 2)
    elif (NbAO + NbAI + NbDO + NbDI) >= 32 :
        coutMES = round(8 * THO, 2)
    else :
        coutMES = round(4 * THO, 2)

    # Calcul CRT
    if (NbAO + NbAI + NbDO + NbDI) >= 40 :
        coutCRT = round(8 * THO, 2)
    else :
        coutCRT = round(4 * THO, 2)



    coutPresta = coutAF + coutProg + coutIHM + coutMES + coutCRT

    Prestation.objects.create(
        user = request.user.username,
        coutAF = coutAF,
        coutProg = coutProg,
        coutIHM = coutIHM,
        coutMES = coutMES,
        coutCRT = coutCRT,
        coutToT = coutPresta
    )

    prestation = Prestation.objects.filter(user = request.user.username)
    for p in prestation:
        print("Coût total prestation automate: ", p.coutToT, "€")


