from django.forms import CharField, IntegerField
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.Typology.modelsEquip import LotIOT, Point
from ..models.Pack.modelsPacks import PackTG, PackOPT, PackIOTUnit
from math import *
from ..models.Pack.modelsAutom import Automate, Prestation
from ..configAutom.configWIT import configWIT
from ..configAutom.configPROG import configPROG

class packValide():
    Reference: CharField(max_length=200)
    AIreserve:IntegerField() 
    DIreserve:IntegerField() 
    AOreserve:IntegerField() 
    DOreserve:IntegerField() 

def newConfig(request):
    message = ""
    
    packsTG = PackTG.objects.all()
    packsOPT = PackOPT.objects.all()
    packsTLR = PackIOTUnit.objects.all()
    
    packsTGValide = []
    packsOPTValide = []
    
    packTGOK = {
            "Reference" : "",
            "AI" : 0,
            "DI" : 0,
            "AO" : 0,
            "DO" : 0,                
            "AIres" : 9999,
            "DIres" : 9999,
            "AOres" : 9999,
            "DOres" : 9999,
            "priceWIT" : 0,
            "priceDISTECH" : 0,
            "priceTREND" : 0,
            "priceSOFREL" : 0,
            "priceMOY" : 0,
        }
    
    packOPTOK = {
        "Reference" : "",
        "Tamb" : 9999,
        "TECS" : 9999,
        "pricePAS" : 0,
        "priceTamb" : 0,
        "priceTECS" : 0,
        "priceTOT" : 0,
    }

    packIOTOK = {
        "Quant_PASS6" : 0,
        "Quant_PASS" : 0,
        "Quant_TAMB" : 0,
        "Quant_TEAU2" : 0,
        "Quant_CO2" : 0,
        "Quant_CPTGAZ" : 0,
        "Quant_CPTELEC" : 0,
        "Quant_CPTCALO" : 0,
        "Quant_CPTEAU" : 0,
        "Prix_PASS6" : 0,
        "Prix_PASS" : 0,
        "Prix_TAMB" : 0,
        "Prix_TEAU2" : 0,
        "Prix_CO2" : 0,
        "Prix_CPTGAZ" : 0,
        "Prix_CPTELEC" : 0,
        "Prix_CPTCALO" : 0,
        "Prix_CPTEAU" : 0,
        "Prix_TOTAL": 0
    }

    # Détermination du pack de TELEGESTION
    if len(Point.objects.filter(user=request.user.username))>1:
        
        nbAI = Point.objects.filter(user=request.user.username, type='TOTAL').values('TM')[0]['TM']
        nbDI = Point.objects.filter(user=request.user.username, type='TOTAL').values('TS')[0]['TS']
        nbAO = Point.objects.filter(user=request.user.username, type='TOTAL').values('TR')[0]['TR']
        nbDO = Point.objects.filter(user=request.user.username, type='TOTAL').values('TC')[0]['TC']

        liste = Point.objects.filter(user=request.user.username)
        nbMbus = 0
        nbModbus = 0
        for p in liste:
            if p.equip == "Compteurs" and p.Mbus > 0:
                nbMbus += 1
            if p.equip == "Compteurs" and p.Modbus > 0:
                nbModbus += 1 

        if nbAI > 0 or nbDI > 0 or nbAO > 0 or nbDO > 0:
            for p in packsTG:
                if nbAI <= p.AI and nbDI <= p.DI and nbAO <= p.AO and nbDO <= p.DO:
                    packsTGValide.append([p.Reference, p.AI-nbAI, p.DI-nbDI, p.AO-nbAO, p.DO-nbDO])

            if len(packsTGValide) > 1:
                for p in packsTGValide:
                    if (int(p[1])<=int(packTGOK.get("AIres"))):
                        if (int(p[3])<=int(packTGOK.get("AOres"))):
                            if (int(p[2])<=int(packTGOK.get("DIres"))):
                                if (int(p[4])<=int(packTGOK.get("DOres"))):
                                    packTGOK["Reference"] = p[0]
                                    packTGOK["AIres"] = int(p[1])
                                    packTGOK["DIres"] = int(p[2])
                                    packTGOK["AOres"] = int(p[3])
                                    packTGOK["DOres"] = int(p[4])
                
                for p in packsTG:
                    if packTGOK["Reference"] == p.Reference:
                        packTGOK["AI"] = p.AI
                        packTGOK["DI"] = p.DI
                        packTGOK["AO"] = p.AO
                        packTGOK["DO"] = p.DO
                        packTGOK["priceWIT"] = p.priceWIT
                        packTGOK["priceDISTECH"] = p.priceDISTECH
                        packTGOK["priceTREND"] = p.priceTREND
                        packTGOK["priceSOFREL"] = p.priceSOFREL
                        packTGOK["priceMOY"] = p.priceMOY
            else:
                # Dimensionnement d'un automate si aucun pack existant
                configWIT(request, request.user.username, True, nbMbus)
                configPROG(request, request.user.username)
                automate = Automate.objects.filter(user=request.user.username)

                AI_Automate = 0
                DI_Automate = 0
                AO_Automate = 0
                DO_Automate = 0

                for carte in automate:
                    AI_Automate += carte.AI 
                    DI_Automate += carte.DI 
                    AO_Automate += carte.AO 
                    DO_Automate += carte.DO + carte.DOR


                prestation = Prestation.objects.filter(user=request.user.username).values('coutToT')[0]['coutToT']
                print(prestation)

                packTGOK["Reference"] = "Automate dimensionné"
                packTGOK["AI"] = AI_Automate
                packTGOK["DI"] = DI_Automate
                packTGOK["AO"] = AO_Automate
                packTGOK["DO"] = DO_Automate
                packTGOK["AIres"] = AI_Automate - nbAI
                packTGOK["DIres"] = DI_Automate - nbDI
                packTGOK["AOres"] = AO_Automate - nbAO
                packTGOK["DOres"] = DO_Automate - nbDO
                packTGOK["priceWIT"] = round(Automate.objects.filter(user=request.user.username).values('cout')[0]['cout'] + Prestation.objects.filter(user=request.user.username).values('coutToT')[0]['coutToT'], 2)
                packTGOK["priceDISTECH"] = 0
                packTGOK["priceTREND"] = 0
                packTGOK["priceSOFREL"] = 0
                packTGOK["priceMOY"] = 0

        else:
            packTGOK["Reference"] = ""
            packTGOK["AI"] = 0
            packTGOK["DI"] = 0
            packTGOK["AO"] = 0
            packTGOK["DO"] = 0
            packTGOK["AIres"] = 0
            packTGOK["DIres"] = 0
            packTGOK["AOres"] = 0
            packTGOK["DOres"] = 0
            packTGOK["priceWIT"] = 0
            packTGOK["priceDISTECH"] = 0
            packTGOK["priceTREND"] = 0
            packTGOK["priceSOFREL"] = 0
            packTGOK["priceMOY"] = 0

    else:
        packTGOK["Reference"] = ""
        packTGOK["AI"] = 0
        packTGOK["DI"] = 0
        packTGOK["AO"] = 0
        packTGOK["DO"] = 0
        packTGOK["AIres"] = 0
        packTGOK["DIres"] = 0
        packTGOK["AOres"] = 0
        packTGOK["DOres"] = 0
        packTGOK["priceWIT"] = 0
        packTGOK["priceDISTECH"] = 0
        packTGOK["priceTREND"] = 0
        packTGOK["priceSOFREL"] = 0
        packTGOK["priceMOY"] = 0


    try:
        #Si l'objet 1 est existant alors on le récupère
        iot = LotIOT.objects.get(user=request.user.username)
        nbTambIOT = iot.nbTempAmbIOT
        nbTECSIOT = iot.nbTemp2EauIOT
        Passerelle = iot.Passerelle
    except LotIOT.DoesNotExist:
        #Si l'objet 1 n'existe pas
        nbTambIOT = 0
        nbTECSIOT = 0
    
    nbIOT  = iot.nbTempAmbIOT + nbTECSIOT + iot.nbCO2IOT + iot.nbTLRElecIOT + iot.nbTLRCaloIOT + iot.nbTLREauIOT
    
    # Détermination du pack d'OPTIMISATION
    if (nbTambIOT > 0 or nbTECSIOT > 0) and Passerelle :
        
        for p in packsOPT:
            if nbTambIOT <= p.Tamb and nbTECSIOT <= p.TECS and p.nbIOTmax > nbIOT :
                packsOPTValide.append([p.Reference, p.Tamb, p.TECS])

        for p in packsOPTValide:
                if (int(p[1])<=int(packOPTOK.get("Tamb")) and int(p[1])-nbTambIOT<=ceil(10*int(p[1])/100)):
                    if (int(p[2])<=int(packOPTOK.get("TECS"))):
                                packOPTOK["Reference"] = p[0]
            
        for p in packsOPT:
            if packOPTOK["Reference"] == p.Reference:
                packOPTOK["Tamb"] = p.Tamb
                packOPTOK["TECS"] = p.TECS
                packOPTOK["pricePAS"] = p.pricePAS
                packOPTOK["priceTamb"] = p.priceTamb
                packOPTOK["priceTECS"] = p.priceTECS
                packOPTOK["priceTOT"] = p.priceTOT

    else:
        packOPTOK["Reference"] = ""
        packOPTOK["Tamb"] = 0
        packOPTOK["TECS"] = 0
        packOPTOK["pricePAS"] = 0
        packOPTOK["priceTamb"] = 0
        packOPTOK["priceTECS"] = 0
        packOPTOK["priceTOT"] = 0
            
    if not Passerelle:
        packIOTOK["Quant_TAMB"] = nbTambIOT
        packIOTOK["Quant_TEAU2"] = nbTECSIOT
    else:
        packIOTOK["Quant_TAMB"] = 0
        packIOTOK["Quant_TEAU2"] = 0

    packIOTOK["Quant_CO2"] = iot.nbCO2IOT
    packIOTOK["Quant_CPTGAZ"] = iot.nbTLRGazIOT
    packIOTOK["Quant_CPTELEC"] = iot.nbTLRElecIOT
    packIOTOK["Quant_CPTCALO"] = iot.nbTLRCaloIOT
    packIOTOK["Quant_CPTEAU"] = iot.nbTLREauIOT

    if Passerelle and nbIOT > 0 and nbIOT <=6 and nbTambIOT==0 and nbTECSIOT==0:
        packIOTOK["Quant_PASS6"] = 1
    elif Passerelle and nbIOT > 6 and nbTambIOT==0 and nbTECSIOT==0:
        packIOTOK["Quant_PASS"] = 1

    for p in packsTLR:
            if p.type == "PASS":
                packIOTOK["Prix_PASS"] = round(packIOTOK["Quant_PASS"] * p.price, 2)
            elif p.type == "PASS6":
                packIOTOK["Prix_PASS6"] = round(packIOTOK["Quant_PASS6"] * p.price, 2)
            if p.type == "CO2":
                packIOTOK["Prix_CO2"] = round(packIOTOK["Quant_CO2"] * p.price, 2)
            if p.type == "TEAU2":
                packIOTOK["Prix_TEAU2"] = round(packIOTOK["Quant_TEAU2"] * p.price, 2)
            if p.type == "TAMB":
                packIOTOK["Prix_TAMB"] = round(packIOTOK["Quant_TAMB"] * p.price, 2)
            if p.type == "CPT GAZ":
                packIOTOK["Prix_CPTGAZ"] = round(packIOTOK["Quant_CPTGAZ"] * p.price, 2)
            if p.type == "CPT ELEC":
                packIOTOK["Prix_CPTELEC"] = round(packIOTOK["Quant_CPTELEC"] * p.price, 2)
            if p.type == "CPT CALO":
                packIOTOK["Prix_CPTCALO"] = round(packIOTOK["Quant_CPTCALO"] * p.price, 2)
            if p.type == "CPT EAU":
                packIOTOK["Prix_CPTEAU"] = round(packIOTOK["Quant_CPTEAU"] * p.price, 2)

    packIOTOK["Prix_TOTAL"] = round(packIOTOK["Prix_CO2"]+packIOTOK["Prix_TEAU2"]+packIOTOK["Prix_TAMB"]+packIOTOK["Prix_CPTGAZ"]+packIOTOK["Prix_CPTELEC"]+ \
        packIOTOK["Prix_CPTCALO"]+packIOTOK["Prix_CPTEAU"], 2)

    print("pack ", packTGOK["Reference"])

    return render(request, 'polls/config.html', {
        'message': message,
        'packTGOK' : packTGOK,
        'packOPTOK' : packOPTOK,
        'packIOTOK' : packIOTOK
        })
