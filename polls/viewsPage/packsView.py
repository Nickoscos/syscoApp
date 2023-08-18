from django.shortcuts import render
from django.shortcuts import redirect
from ..models.Typology.modelsEquip import Liste
from ..models.Pack.modelsPacks import listePacks, Pack

def choixPack(request):
    message = ''
    
    print("requete:", request)
    if request.user.username != "":
        #Création d'un unique objet chaufferie dans la base de données  
        try:
            #Si l'objet 1 est existant alors on le récupère
            listePack = listePacks.objects.get(id=1)
        except listePacks.DoesNotExist:
            #Si l'objet 1 n'existe pas, on l'initialise
            print("create")
            listePack = listePacks.objects.create(id=1)
            listePack.save()

        # listePack = genListePack()
        if request.method == "POST":
            print("post")
            if(request.POST.get("form_type") == "listPackform"):
                if request.POST.get("Add") != None:
                    print("add")
                    pack = Pack(
                        Reference = request.POST.get('reference_Add'), 
                        AI = int(request.POST.get('AI_Add')), 
                        DI = int(request.POST.get('DI_Add')), 
                        AO = int(request.POST.get('AO_Add')), 
                        DO = int(request.POST.get('DO_Add')), 
                        priceWIT=int(request.POST.get('priceWIT_Add')), 
                        priceTREND=int(request.POST.get('priceTREND_Add')), 
                        priceDISTECH=int(request.POST.get('priceDISTECH_Add')), 
                        priceSOFREL=int(request.POST.get('priceSOFREL_Add')), 
                        priceMOY=int(request.POST.get('priceMOY_Add'))
                        )
                    listePack.pack.append(pack)
                    listePack.save
                elif request.POST.get("Supp") != None:
                    listePack.pack.pop(int(request.POST.get('Supp')))
                    listePack.save

        return render(request, 'polls/packs.html', {
            'message': message,
            'listePack': listePack
            })
    else :
        return render(request, "registration/login.html")
    
def addPack():
    listePack = listePacks
    # Ajout d'un pack
    if len(listePack.pack) > 0:
        for i in listePack.pack:
            if i.Reference == "REG1":
                print("pack existant")
            else:
                listePack.pack.append(Pack(
                    Reference = "REG1",
                    AI = 10,
                    DI = 22,
                    AO = 9,
                    DO = 9,
                    priceWIT = 7344.74,
                    priceTREND = 8270.98,
                    priceDISTECH = 6105.65,
                    priceSOFREL = 7121.58,
                    priceMOY = 7210.74
                )) 
    else:
        print('ajout')
        listePack.pack.append(Pack(
                    Reference = "REG1",
                    AI = 10,
                    DI = 22,
                    AO = 9,
                    DO = 9,
                    priceWIT = 7344.74,
                    priceTREND = 8270.98,
                    priceDISTECH = 6105.65,
                    priceSOFREL = 7121.58,
                    priceMOY = 7210.74
                )) 
    
    return listePack

def genListePack():
    listePack = listePacks
    # Ajout d'un pack
    if len(listePack.pack) > 0:
        for i in listePack.pack:
            if i.Reference == "REG1":
                print("pack existant")
            else:
                listePack.pack.append(Pack(
                    Reference = "REG1",
                    AI = 10,
                    DI = 22,
                    AO = 9,
                    DO = 9,
                    priceWIT = 7344.74,
                    priceTREND = 8270.98,
                    priceDISTECH = 6105.65,
                    priceSOFREL = 7121.58,
                    priceMOY = 7210.74
                )) 
    else:
        print('ajout')
        listePack.pack.append(Pack(
                    Reference = "REG1",
                    AI = 10,
                    DI = 22,
                    AO = 9,
                    DO = 9,
                    priceWIT = 7344.74,
                    priceTREND = 8270.98,
                    priceDISTECH = 6105.65,
                    priceSOFREL = 7121.58,
                    priceMOY = 7210.74
                )) 
    
    return listePack