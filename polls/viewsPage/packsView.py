from django.shortcuts import redirect, render
from ..models.Pack.modelsPacks import PackTG, PackOPT, PackIOTUnit

def listPack(request):
    message = ''

    packsTG = PackTG.objects.all()
    packsOPT = PackOPT.objects.all()
    packsIOTUnit = PackIOTUnit.objects.all()
    
    if request.method == "POST":
        if(request.POST.get("form_type") == "listPackTGform"):
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
            elif request.POST.get("Supp") != None:
                packdel = packsTG.get(Reference=request.POST.get('Supp'))
                packdel.delete()

        if(request.POST.get("form_type") == "listPackOPTform"):
            if request.POST.get("Add") != None:
                if not PackOPT.objects.filter(Reference=request.POST.get('reference_Add')).exists():
                    packsOPT.create(Reference = request.POST.get('reference_Add'), 
                        Tamb = int(request.POST.get('Tamb_Add')), 
                        TECS = int(request.POST.get('TECS_Add')), 
                        pricePAS=float(request.POST.get('pricePAS_Add')), 
                        priceTamb=float(request.POST.get('priceTamb_Add')), 
                        priceTECS=float(request.POST.get('priceTECS_Add')), 
                        priceTOT=float(request.POST.get('priceTOT_Add')))
                else:
                    message = "pack existant"
            elif request.POST.get("Supp") != None:
                packdel = packsOPT.get(Reference=request.POST.get('Supp'))
                packdel.delete()

    return render(request, 'polls/packs.html', {
        'message': message,
        'packsTG': packsTG,
        'packsOPT': packsOPT,
        'packsIOT': packsIOTUnit,
        })

