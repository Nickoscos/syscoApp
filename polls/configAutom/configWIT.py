from ..models.Typology.modelsEquip import Point
from ..models.Pack.modelsAutom import Automate
from ..models.Pack.modelsAutom import carteAutom

def configWIT(request, username, modemNec):
    liste = Point.objects.filter(user=username)
    catalogue = carteAutom.objects.all()
    print("config automate")

    try:
        Automate.objects.filter(user=request.user.username).delete()
    except Automate.DoesNotExist:
        automate = Automate.objects.create(user=request.user.username)

    if len(liste)>1 :
        #Ajout de la CPU dans la configuration
        # Etape 1: On parcoure le catalogue en fonction du type de la carte recherchée
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
                    print(carte.reference)
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
                    print(carte.reference)
    
    