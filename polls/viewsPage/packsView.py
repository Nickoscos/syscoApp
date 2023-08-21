from django.shortcuts import render
from django.shortcuts import redirect
from ..models.Typology.modelsEquip import Liste
from ..models.Pack.modelsPacks import listePacks, PackTG, PackOPT

def choixPack(request):
    message = ''

    print("requete:", request)
    if request.user.username != "":
        packsTG = PackTG.objects.all()
        packsOPT = PackOPT.objects.all()
        
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
            'packsOPT': packsOPT
            })
    else :
        return render(request, "registration/login.html")
    
# def addPack():
#     listePack = listePacks
#     # Ajout d'un pack
#     if len(listePack.pack) > 0:
#         for i in listePack.pack:
#             if i.Reference == "REG1":
#                 print("pack existant")
#             else:
#                 listePack.pack.append(Pack(
#                     Reference = "REG1",
#                     AI = 10,
#                     DI = 22,
#                     AO = 9,
#                     DO = 9,
#                     priceWIT = 7344.74,
#                     priceTREND = 8270.98,
#                     priceDISTECH = 6105.65,
#                     priceSOFREL = 7121.58,
#                     priceMOY = 7210.74
#                 )) 
#     else:
#         print('ajout')
#         listePack.pack.append(Pack(
#                     Reference = "REG1",
#                     AI = 10,
#                     DI = 22,
#                     AO = 9,
#                     DO = 9,
#                     priceWIT = 7344.74,
#                     priceTREND = 8270.98,
#                     priceDISTECH = 6105.65,
#                     priceSOFREL = 7121.58,
#                     priceMOY = 7210.74
#                 )) 
    
#     return listePack

# def genListePack():
#     listePack = listePacks
#     # Ajout d'un pack
#     if len(listePack.pack) > 0:
#         for i in listePack.pack:
#             if i.Reference == "REG1":
#                 print("pack existant")
#             else:
#                 listePack.pack.append(Pack(
#                     Reference = "REG1",
#                     AI = 10,
#                     DI = 22,
#                     AO = 9,
#                     DO = 9,
#                     priceWIT = 7344.74,
#                     priceTREND = 8270.98,
#                     priceDISTECH = 6105.65,
#                     priceSOFREL = 7121.58,
#                     priceMOY = 7210.74
#                 )) 
#     else:
#         print('ajout')
#         listePack.pack.append(Pack(
#                     Reference = "REG1",
#                     AI = 10,
#                     DI = 22,
#                     AO = 9,
#                     DO = 9,
#                     priceWIT = 7344.74,
#                     priceTREND = 8270.98,
#                     priceDISTECH = 6105.65,
#                     priceSOFREL = 7121.58,
#                     priceMOY = 7210.74
#                 )) 
    
#     return listePack