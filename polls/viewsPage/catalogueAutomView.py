from django.shortcuts import redirect, render
from ..models.Pack.modelsAutom import carteAutom

def catalogueAutom(request):
    message = ''

    cartes = carteAutom.objects.all()


    carteUPDATE_ref = ""
    if request.method == "POST":
        #Catalogue automate
        if(request.POST.get("form_type") == "catalogueWITAddform"):
            if request.POST.get("Add") != None:
                if not carteAutom.objects.filter(reference=request.POST.get('reference_Add')).exists():
                    cartes.create( type = request.POST.get('type_Add'),
                        reference = request.POST.get('reference_Add'),  
                        DI = int(request.POST.get('DI_Add')), 
                        DO = int(request.POST.get('DO_Add')),
                        AI = int(request.POST.get('AI_Add')),
                        AO = int(request.POST.get('AO_Add')), 
                        UI = int(request.POST.get('UI_Add')),
                        UO = int(request.POST.get('UO_Add')),
                        DOR = int(request.POST.get('DOR_Add')),
                        DO_UO = int(request.POST.get('DO_UO_Add')),
                        nbEmpl = int(request.POST.get('nbEmpl_Add')),
                        extension = bool(request.POST.get('extension_Add')),
                        rs232 = int(request.POST.get('rs232_Add')), 
                        rs485 = int(request.POST.get('rs485_Add')), 
                        ressources = int(request.POST.get('ressources_Add')), 
                        maxModbus = int(request.POST.get('maxModbus_Add')), 
                        Imagerie = bool(request.POST.get('Imagerie_Add')), 
                        maxMbus = int(request.POST.get('maxMbus_Add')), 
                        prix=float(request.POST.get('prix_Add')))
                else:
                    message = "référence carte existante"
        elif(request.POST.get("form_type") == "catalogueWITSuppform"):           
            if request.POST.get("Supp") != None:
                cartedel = cartes.get(reference=request.POST.get('Supp'))
                cartedel.delete()
        
        if(request.POST.get("form_type") == "catalogueWITModifform"):    
            if request.POST.get("Modif") != None:
                carteUPDATE_ref = request.POST.get("Modif")
        elif(request.POST.get("form_type") == "catalogueWITUPGform"):   
            if request.POST.get("ValidModif") != None:
                print(request.POST.get("ValidModif"))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(type=request.POST.get('type_Upd'))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(reference=request.POST.get('reference_Upd'))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(DI=int(request.POST.get('DI_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(DO=int(request.POST.get('DO_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(AI=int(request.POST.get('AI_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(AO=int(request.POST.get('AO_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(UI=int(request.POST.get('UI_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(UO=int(request.POST.get('UO_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(DOR=int(request.POST.get('DOR_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(DO_UO=int(request.POST.get('DO_UO_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(nbEmpl=int(request.POST.get('nbEmpl_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(extension=bool(request.POST.get('extension_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(rs232=int(request.POST.get('rs232_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(rs485=int(request.POST.get('rs485_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(ressources=int(request.POST.get('ressources_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(maxModbus=int(request.POST.get('maxModbus_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(Imagerie=bool(request.POST.get('Imagerie_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(maxMbus=int(request.POST.get('maxMbus_Upd')))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(prix=float(request.POST.get('prix_Upd').replace(",",".")))


    return render(request, 'polls/catalogueAutomate.html', {
        'message': message,
        'catalogueWIT': cartes,
        'itemUPDATE': carteUPDATE_ref,
        })

