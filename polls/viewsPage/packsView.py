from django.shortcuts import redirect, render
from ..models.Pack.modelsPacks import PackTG, PackOPT, PackIOTUnit

def listPack(request):
    message = ''

    packsTG = PackTG.objects.all()
    packsOPT = PackOPT.objects.all()
    packsIOTUnit = PackIOTUnit.objects.all()

    packUPDATE_ref = ""
    if request.method == "POST":
        #PACKS TELEGESTION
        if(request.POST.get("form_type") == "PackTGAddform"):
            if request.POST.get("Add") != None:
                if not PackTG.objects.filter(Reference=request.POST.get('reference_Add')).exists():
                    packsTG.create(Reference = request.POST.get('reference_Add'), 
                        AI = int(request.POST.get('AI_Add')), 
                        DI = int(request.POST.get('DI_Add')), 
                        AO = int(request.POST.get('AO_Add')), 
                        DO = int(request.POST.get('DO_Add')), 
                        priceWIT=float(request.POST.get('priceWIT_Add')), 
                        priceTREND=float(request.POST.get('priceTREND_Add')), 
                        priceDISTECH=float(request.POST.get('priceDISTECH_Add')), 
                        priceSOFREL=float(request.POST.get('priceSOFREL_Add')), 
                        priceMOY=float(request.POST.get('priceMOY_Add')))
                else:
                    message = "pack existant"
        elif(request.POST.get("form_type") == "PackTGSuppform"):           
            if request.POST.get("Supp") != None:
                packdel = packsTG.get(Reference=request.POST.get('Supp'))
                packdel.delete()
        
        if(request.POST.get("form_type") == "PackTGModifform"):    
            if request.POST.get("Modif") != None:
                packUPDATE_ref = request.POST.get("Modif")
        elif(request.POST.get("form_type") == "PackTGUPGform"):   
            if request.POST.get("ValidModif") != None:
                print(request.POST.get("ValidModif"))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(AI=int(request.POST.get('AI_Upd')))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(DI=int(request.POST.get('DI_Upd')))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(AO=int(request.POST.get('AO_Upd')))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(DO=int(request.POST.get('DO_Upd')))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(priceWIT=float(request.POST.get('priceWIT_Upd').replace(",",".")))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(priceTREND=float(request.POST.get('priceTREND_Upd').replace(",",".")))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(priceDISTECH=float(request.POST.get('priceDISTECH_Upd').replace(",",".")))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(priceSOFREL=float(request.POST.get('priceSOFREL_Upd').replace(",",".")))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(priceMOY=float(request.POST.get('priceMOY_Upd').replace(",",".")))
                PackTG.objects.filter(Reference=request.POST.get("ValidModif")).update(Reference=request.POST.get('reference_Upd'))

        #PACKS OPTIMISATION
        if(request.POST.get("form_type") == "PackOPTAddform"):
            if request.POST.get("Add") != None:
                if not PackOPT.objects.filter(Reference=request.POST.get('reference_Add')).exists():
                    packsOPT.create(Reference = request.POST.get('reference_Add'), 
                        nbIOTmax = int(request.POST.get('nbIOTmax_Add')),           
                        Tamb = int(request.POST.get('Tamb_Add')), 
                        TECS = int(request.POST.get('TECS_Add')), 
                        pricePAS=float(request.POST.get('pricePAS_Add')), 
                        priceTamb=float(request.POST.get('priceTamb_Add')), 
                        priceTECS=float(request.POST.get('priceTECS_Add')), 
                        priceTOT=float(request.POST.get('priceTOT_Add')))
                else:
                    message = "pack existant"
        elif (request.POST.get("form_type") == "PackOPTSuppform"):
            packdel = packsOPT.get(Reference=request.POST.get('Supp'))
            packdel.delete()

        if(request.POST.get("form_type") == "PackOPTModifform"):
            if request.POST.get("Modif") != None:
                packUPDATE_ref = request.POST.get("Modif")
        elif(request.POST.get("form_type") == "PackOPTUPGform"):   
            if request.POST.get("ValidModif") != None:
                print(request.POST.get("ValidModif"))
                PackOPT.objects.filter(Reference=request.POST.get("ValidModif")).update(nbIOTmax=int(request.POST.get('nbIOTmax_Upd')))
                PackOPT.objects.filter(Reference=request.POST.get("ValidModif")).update(Tamb=int(request.POST.get('Tamb_Upd')))
                PackOPT.objects.filter(Reference=request.POST.get("ValidModif")).update(TECS=int(request.POST.get('TECS_Upd')))
                PackOPT.objects.filter(Reference=request.POST.get("ValidModif")).update(pricePAS=float(request.POST.get('pricePAS_Upd').replace(",",".")))
                PackOPT.objects.filter(Reference=request.POST.get("ValidModif")).update(priceTamb=float(request.POST.get('priceTamb_Upd').replace(",",".")))
                PackOPT.objects.filter(Reference=request.POST.get("ValidModif")).update(priceTECS=float(request.POST.get('priceTECS_Upd').replace(",",".")))
                PackOPT.objects.filter(Reference=request.POST.get("ValidModif")).update(priceTOT=float(request.POST.get('priceTOT_Upd').replace(",",".")))
                PackOPT.objects.filter(Reference=request.POST.get("ValidModif")).update(Reference=request.POST.get('reference_Upd'))
        
        #PACKS IOT
        if(request.POST.get("form_type") == "PackIOTAddform"):
            if request.POST.get("Add") != None:
                if not PackIOTUnit.objects.filter(Reference=request.POST.get('referenceIOT_Add')).exists():
                    packsIOTUnit.create(Reference = request.POST.get('referenceIOT_Add'), 
                        type = request.POST.get('typeIOT_Add'), 
                        comment = request.POST.get('commentIOT_Add'), 
                        price=request.POST.get('priceIOT_Add'))
                else:
                    message = "pack existant"
        elif (request.POST.get("form_type") == "PackIOTSuppform"):
            packdel = packsOPT.get(Reference=request.POST.get('Supp'))
            packdel.delete()

        if(request.POST.get("form_type") == "PackIOTModifform"):
            if request.POST.get("Modif") != None:
                packUPDATE_ref = request.POST.get("Modif")
        elif(request.POST.get("form_type") == "PackIOTUPGform"):   
            if request.POST.get("ValidModif") != None:
                print(request.POST.get("ValidModif"))
                PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(type=request.POST.get('typeIOT_Upd'))
                PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(comment=request.POST.get('commentIOT_Upd'))
                PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(price=float(request.POST.get('priceIOT_Upd').replace(",",".")))
                PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(Reference=request.POST.get('reference_Upd'))


    return render(request, 'polls/packs.html', {
        'message': message,
        'packsTG': packsTG,
        'packsOPT': packsOPT,
        'packsIOTUnit': packsIOTUnit,
        'packUPDATE' : packUPDATE_ref,
        })

