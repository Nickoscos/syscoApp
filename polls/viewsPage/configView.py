from django.forms import CharField, IntegerField
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.Typology.modelsEquip import LotIOT, Point
from ..models.Pack.modelsPacks import PackTG, PackOPT

class packValide():
    Reference: CharField(max_length=200)
    AIreserve:IntegerField() 
    DIreserve:IntegerField() 
    AOreserve:IntegerField() 
    DOreserve:IntegerField() 

def newConfig(request):
    message = ""
    print("config")
    packsTG = PackTG.objects.all()
    packsOPT = PackOPT.objects.all()
    
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

    if len(Point.objects.filter(user=request.user.username))>1:
        
        nbAI = Point.objects.filter(user=request.user.username, type='TOTAL').values('TM')[0]['TM']
        nbDI = Point.objects.filter(user=request.user.username, type='TOTAL').values('TS')[0]['TS']
        nbAO = Point.objects.filter(user=request.user.username, type='TOTAL').values('TR')[0]['TR']
        nbDO = Point.objects.filter(user=request.user.username, type='TOTAL').values('TC')[0]['TC']

        if nbAI > 0 or nbDI > 0 or nbAO > 0 or nbDO > 0:
            for p in packsTG:
                if nbAI <= p.AI and nbDI <= p.DI and nbAO <= p.AO and nbDO <= p.DO:
                    packsTGValide.append([p.Reference, p.AI-nbAI, p.DI-nbDI, p.AO-nbAO, p.DO-nbDO])

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
    except LotIOT.DoesNotExist:
        #Si l'objet 1 n'existe pas
        nbTambIOT = 0
        nbTECSIOT = 0
    
    if nbTambIOT > 0 or nbTECSIOT > 0 :
        for p in packsOPT:
            if nbTambIOT <= p.Tamb and nbTECSIOT <= p.TECS :
                packsOPTValide.append([p.Reference, p.Tamb-nbTambIOT, p.TECS-nbTECSIOT])

        for p in packsOPTValide:
            if (int(p[1])<=int(packOPTOK.get("Tamb"))):
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
            
    return render(request, 'polls/config.html', {
        'message': message,
        'packTGOK' : packTGOK,
        'packOPTOK' : packOPTOK,
        })
