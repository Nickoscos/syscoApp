from django.forms import CharField, IntegerField
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.Typology.modelsEquip import Liste
from ..models.Pack.modelsPacks import PackTG, PackOPT

class packValide():
    Reference: CharField(max_length=200)
    AIreserve:IntegerField() 
    DIreserve:IntegerField() 
    AOreserve:IntegerField() 
    DOreserve:IntegerField() 

def newConfig(request):
    message = ""

    # if request.user.username != "":
    packsTG = PackTG.objects.all()
    packsOPT = PackOPT.objects.all()
    
    packsValide = []

    if len(Liste(user=request.user.username).pts)>1:
        liste = Liste(user=request.user.username)
        nbAI = liste.pts[-1].TM
        nbDI = liste.pts[-1].TS
        nbAO = liste.pts[-1].TR
        nbDO = liste.pts[-1].TC
        for p in packsTG:
            if nbAI <= p.AI and nbDI <= p.DI and nbAO <= p.AO and nbDO <= p.DO:
                packsValide.append([p.Reference, p.AI-nbAI, p.DI-nbDI, p.AO-nbAO, p.DO-nbDO])
        
        packOK = {
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

        for p in packsValide:
            if (int(p[1])<=int(packOK.get("AIres"))):
                if (int(p[3])<=int(packOK.get("AOres"))):
                    if (int(p[2])<=int(packOK.get("DIres"))):
                        if (int(p[4])<=int(packOK.get("DOres"))):
                            packOK["Reference"] = p[0]
                            packOK["AIres"] = int(p[1])
                            packOK["DIres"] = int(p[2])
                            packOK["AOres"] = int(p[3])
                            packOK["DOres"] = int(p[4])
        
        for p in packsTG:
            if packOK["Reference"] == p.Reference:
                packOK["AI"] = p.AI
                packOK["DI"] = p.DI
                packOK["AO"] = p.AO
                packOK["DO"] = p.DO
                packOK["priceWIT"] = p.priceWIT
                packOK["priceDISTECH"] = p.priceDISTECH
                packOK["priceTREND"] = p.priceTREND
                packOK["priceSOFREL"] = p.priceSOFREL
                packOK["priceMOY"] = p.priceMOY
    else:
        return redirect("polls:chaufferie")
            
    return render(request, 'polls/config.html', {
        'message': message,
        'packOK' : packOK,
        })
    # else :
    #     return redirect("polls:login")
        # return render(request, "registration/login.html")