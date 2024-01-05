from django.shortcuts import redirect, render
from ..models.Pack.modelsPacks import PackTG, PackOPT, PackIOTUnit
from DEFPTS.settings import MEDIA_URL
import pandas as pd
import mimetypes
from django.http import HttpResponse
import xlsxwriter
from django.core.paginator import Paginator
from datetime import datetime

def accueilCatalogPack(request):
    return render(request, 'polls/accueilCataloguePacks.html')

# PACK TELEGESTION
def packTLG(request):
    message = ''

    packsTG = PackTG.objects.all()
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
        elif(request.POST.get("form_type") == "catalogueSuppform"):           
            if request.POST.get("Supp") != None:
                print(request.POST.get("Supp"))
                packdel = packsTG.get(Reference=request.POST.get('Supp'))
                packdel.delete()
        
        if(request.POST.get("form_type") == "catalogueModifform"):    
            if request.POST.get("Modif") != None:
                print("en cours")
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

        # Soumission du formulaire de téléchargement catalogue
        elif (request.POST.get("form_type") == "exportCatalogue"):
            message = catalogueTLGXls(request, request.user.username)
            fileName = "cataloguePacksTLG" + str(datetime.now() )
            print(fileName)
            return redirect("polls:exportcatalogPacksTLG", filename="cataloguePacksTLG.xlsx", newName=fileName)
        
        # Soumission du formulaire de chargement catalogue
        elif (request.POST.get("form_type") == "importCatalogue"): 
            file = request.FILES['myfile']
            print("chargement du catalogue ", file.name)
            upload_catalogueTLG(request, file)

    #PAGINATION CATALOGUE
    paginator = Paginator(packsTG, 10) # Show 15 packs par page
    page = request.GET.get('page')
    catalogue = paginator.get_page(page)
    print(packUPDATE_ref)
    return render(request, 'polls/cataloguePacksTLG.html', {
        'message': message,
        'catalogue': catalogue,
        'packUPDATE' : packUPDATE_ref,
        })

#Page Upload catalogue TLG
def upload_catalogueTLG(request, file):
    print(file.name)
    fileexcel = pd.read_excel(file, sheet_name='Liste')  

    try:
        PackTG.objects.all().delete()
        
    except PackTG.DoesNotExist:
        print("Catalogue vide")

    print(len(fileexcel))
    catalogue = PackTG.objects.all()
    for index, row in fileexcel.iterrows():
        print(str(row['REFERENCE']))
        if not('nan' in str(row['REFERENCE'])): 
            catalogue.create(
                        Reference= row['REFERENCE'],
                        AI= row['AI'],
                        DI= row['DI'], 
                        AO= row['DI'], 
                        DO= row['DO'], 
                        priceWIT= row['Prix WIT'], 
                        priceTREND= row['Prix TREND'],
                        priceDISTECH= row['Prix DISTECH'],
                        priceSOFREL= row['Prix SOFREL'],
                        priceMOY= row['Prix MOYEN'])    

def catalogueTLGXls(request, username):
    catalogue = PackTG.objects.all()

    #Initialisation du message
    message = ""

    file = MEDIA_URL + "cataloguePacksTLG.xlsx"

    # On crée un nouveau classeur
    with xlsxwriter.Workbook(file) as workbook:

        # On y ajoute une première feuille
        worksheet = workbook.add_worksheet("Liste")

        # On dimensionne les colonnes
        worksheet.set_column("A:A", 20)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 60)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 20)
        worksheet.set_column("G:G", 20)
        worksheet.set_column("H:H", 20)
        worksheet.set_column("I:I", 20)
        worksheet.set_column("J:J", 20)


        # On définit un style qui sera utilisé pour la ligne de titre.
        # Pour obtenir toutes les caractéristiques disponibles : print(dir(header_style))
        header_style = workbook.add_format({
            "bg_color": "gray",
            "font_color": "white",
            "bold": True
        })


        # On injecte la ligne de titre dans la première feuille    
        worksheet.write("A1", "REFERENCE", header_style)
        worksheet.write("B1", "AI", header_style)
        worksheet.write("C1", "DI", header_style)
        worksheet.write("D1", "AO", header_style)
        worksheet.write("E1", "DO", header_style)
        worksheet.write("F1", "Prix WIT", header_style)
        worksheet.write("G1", "Prix TREND", header_style)
        worksheet.write("H1", "Prix DISTECH", header_style)
        worksheet.write("I1", "Prix SOFREL", header_style)
        worksheet.write("J1", "Prix MOYEN", header_style)
        worksheet.write("K1", "ACTION", header_style)

        pos = 1
        derniereLigne = pos + len(catalogue)

        for point in catalogue:
            pos = pos + 1
            style = workbook.add_format({
                "bg_color": "white",
                "font_color": "black",
                "bold": False
            })


            worksheet.write("A"+str(pos), point.Reference, style)
            worksheet.write("B"+str(pos), point.AI, style)
            worksheet.write("C"+str(pos), point.DI, style)
            worksheet.write("D"+str(pos), point.AO, style)
            worksheet.write("E"+str(pos), point.DO, style)
            worksheet.write("F"+str(pos), point.priceWIT, style)
            worksheet.write("G"+str(pos), point.priceTREND, style)
            worksheet.write("H"+str(pos), point.priceDISTECH, style)
            worksheet.write("I"+str(pos), point.priceSOFREL, style)
            worksheet.write("J"+str(pos), point.priceMOY, style)
            worksheet.write("K"+str(pos), "", style)


    message = "Catalogue générée"
    return message


# PACK OPTIMISATION IoT
def packOPT(request):
    message = ''

    packsOPT = PackOPT.objects.all()
    packUPDATE_ref = ""

    if request.method == "POST":
        #PACKS OPTIMISATION
        if(request.POST.get("form_type") == "PackOPTAddform"):
            if request.POST.get("Add") != None:
                print(request.POST.get("reference_Add"))
                if not PackOPT.objects.filter(Reference=request.POST.get('reference_Add')).exists():
                    print(request.POST.get("reference_Add"))
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
        elif(request.POST.get("form_type") == "catalogueSuppform"):           
            if request.POST.get("Supp") != None:
                print(request.POST.get("Supp"))
                packdel = packsOPT.get(Reference=request.POST.get('Supp'))
                packdel.delete()
        
        if(request.POST.get("form_type") == "catalogueModifform"):    
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

        # Soumission du formulaire de téléchargement catalogue
        elif (request.POST.get("form_type") == "exportCatalogue"):
            message = catalogueOPTXls(request, request.user.username)
            fileName = "cataloguePacksOPT" + str(datetime.now() )
            print(fileName)
            return redirect("polls:exportcatalogPacksOPT", filename="cataloguePacksOPT.xlsx", newName=fileName)
        
        # Soumission du formulaire de chargement catalogue
        elif (request.POST.get("form_type") == "importCatalogue"): 
            file = request.FILES['myfile']
            print("chargement du catalogue ", file.name)
            upload_catalogueOPT(request, file)

    #PAGINATION CATALOGUE
    paginator = Paginator(packsOPT, 10) # Show 15 packs par page
    page = request.GET.get('page')
    catalogue = paginator.get_page(page)
    return render(request, 'polls/cataloguePacksOPT.html', {
        'message': message,
        'catalogue': catalogue,
        'packUPDATE' : packUPDATE_ref,
        })

#Page Upload catalogue OPTIMISATION IoT
def upload_catalogueOPT(request, file):
    print(file.name)
    fileexcel = pd.read_excel(file, sheet_name='Liste')  

    try:
        PackOPT.objects.all().delete()
        
    except PackOPT.DoesNotExist:
        print("Catalogue vide")

    print(len(fileexcel))
    catalogue = PackOPT.objects.all()
    for index, row in fileexcel.iterrows():
        print(str(row['REFERENCE']))
        if not('nan' in str(row['REFERENCE'])): 
            catalogue.create(
                        Reference= row['REFERENCE'],
                        nbIOTmax= row['Nb IoT MAX'],
                        Tamb= row['Température Ambiant'], 
                        TECS= row['Température ECS'], 
                        pricePAS= row['Prix Passerelle'], 
                        priceTamb= row['Prix Température Ambiant'], 
                        priceTECS= row['Prix Température ECS'],
                        priceTOT= row['Prix TOTAL'])    

def catalogueOPTXls(request, username):
    catalogue = PackOPT.objects.all()

    #Initialisation du message
    message = ""

    file = MEDIA_URL + "cataloguePacksOPT.xlsx"

    # On crée un nouveau classeur
    with xlsxwriter.Workbook(file) as workbook:

        # On y ajoute une première feuille
        worksheet = workbook.add_worksheet("Liste")

        # On dimensionne les colonnes
        worksheet.set_column("A:A", 20)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 60)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 20)
        worksheet.set_column("G:G", 20)
        worksheet.set_column("H:H", 20)
        worksheet.set_column("I:I", 20)

        # On définit un style qui sera utilisé pour la ligne de titre.
        # Pour obtenir toutes les caractéristiques disponibles : print(dir(header_style))
        header_style = workbook.add_format({
            "bg_color": "gray",
            "font_color": "white",
            "bold": True
        })


        # On injecte la ligne de titre dans la première feuille    
        worksheet.write("A1", "REFERENCE", header_style)
        worksheet.write("B1", "Nb IoT MAX", header_style)
        worksheet.write("C1", "Température Ambiant", header_style)
        worksheet.write("D1", "Température ECS", header_style)
        worksheet.write("E1", "Prix Passerelle", header_style)
        worksheet.write("F1", "Prix Température Ambiant", header_style)
        worksheet.write("G1", "Prix Température ECS", header_style)
        worksheet.write("H1", "Prix TOTAL", header_style)
        worksheet.write("I1", "ACTION", header_style)

        pos = 1
        derniereLigne = pos + len(catalogue)

        for point in catalogue:
            pos = pos + 1
            style = workbook.add_format({
                "bg_color": "white",
                "font_color": "black",
                "bold": False
            })
   
            worksheet.write("A"+str(pos), point.Reference, style)
            worksheet.write("B"+str(pos), point.nbIOTmax, style)
            worksheet.write("C"+str(pos), point.Tamb, style)
            worksheet.write("D"+str(pos), point.TECS, style)
            worksheet.write("E"+str(pos), point.pricePAS, style)
            worksheet.write("F"+str(pos), point.priceTamb, style)
            worksheet.write("G"+str(pos), point.priceTECS, style)
            worksheet.write("H"+str(pos), point.priceTOT, style)
            worksheet.write("I"+str(pos), "", style)


    message = "Catalogue générée"
    return message

# PACK TELERELEVE
def packTLR(request):
    message = ''

    packsTLR = PackIOTUnit.objects.all()
    packUPDATE_ref = ""

    if request.method == "POST":
        if(request.POST.get("form_type") == "PackOPTAddform"):
            if request.POST.get("Add") != None:
                print(request.POST.get("reference_Add"))
                if not PackIOTUnit.objects.filter(Reference=request.POST.get('reference_Add')).exists():
                    print(request.POST.get("reference_Add"))
                    packsTLR.create(Reference = request.POST.get('reference_Add'), 
                        type = request.POST.get('type_Add'), 
                        comment = request.POST.get('comment_Add'), 
                        price=request.POST.get('price_Add'))
                else:
                    message = "pack existant"
        elif(request.POST.get("form_type") == "catalogueSuppform"):           
            if request.POST.get("Supp") != None:
                print(request.POST.get("Supp"))
                packdel = packsTLR.get(Reference=request.POST.get('Supp'))
                packdel.delete()
        
        if(request.POST.get("form_type") == "catalogueModifform"):    
            if request.POST.get("Modif") != None:
                packUPDATE_ref = request.POST.get("Modif")
        elif(request.POST.get("form_type") == "PackTLRUPGform"):   
            if request.POST.get("ValidModif") != None:
                PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(type=request.POST.get('type_Upd'))
                PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(comment=request.POST.get('comment_Upd'))
                PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(price=float(request.POST.get('price_Upd').replace(",",".")))
                PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(Reference=request.POST.get('reference_Upd'))

        # Soumission du formulaire de téléchargement catalogue
        elif (request.POST.get("form_type") == "exportCatalogue"):
            message = catalogueTLRXls(request, request.user.username)
            fileName = "cataloguePacksTLR" + str(datetime.now() )
            print(fileName)
            return redirect("polls:exportcatalogPacksTLR", filename="cataloguePacksTLR.xlsx", newName=fileName)
        
        # Soumission du formulaire de chargement catalogue
        elif (request.POST.get("form_type") == "importCatalogue"): 
            file = request.FILES['myfile']
            print("chargement du catalogue ", file.name)
            upload_catalogueTLR(request, file)

    #PAGINATION CATALOGUE
    paginator = Paginator(packsTLR, 10) # Show 15 packs par page
    page = request.GET.get('page')
    catalogue = paginator.get_page(page)
    return render(request, 'polls/cataloguePacksTLR.html', {
        'message': message,
        'catalogue': catalogue,
        'packUPDATE' : packUPDATE_ref,
        })

#Page Upload catalogue TELERELEVE IoT
def upload_catalogueTLR(request, file):
    print(file.name)
    fileexcel = pd.read_excel(file, sheet_name='Liste')  

    try:
        PackIOTUnit.objects.all().delete()
        
    except PackIOTUnit.DoesNotExist:
        print("Catalogue vide")

    print(len(fileexcel))
    catalogue = PackIOTUnit.objects.all()
    for index, row in fileexcel.iterrows():
        print(str(row['REFERENCE']))
        if not('nan' in str(row['REFERENCE'])): 
            catalogue.create(
                        Reference= row['REFERENCE'],
                        type= row['TYPE'],
                        comment= row['COMMENTAIRE'],
                        price= row['PRIX'])    

def catalogueTLRXls(request, username):
    catalogue = PackIOTUnit.objects.all()

    #Initialisation du message
    message = ""

    file = MEDIA_URL + "cataloguePacksTLR.xlsx"

    # On crée un nouveau classeur
    with xlsxwriter.Workbook(file) as workbook:

        # On y ajoute une première feuille
        worksheet = workbook.add_worksheet("Liste")

        # On dimensionne les colonnes
        worksheet.set_column("A:A", 20)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 60)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)

        # On définit un style qui sera utilisé pour la ligne de titre.
        # Pour obtenir toutes les caractéristiques disponibles : print(dir(header_style))
        header_style = workbook.add_format({
            "bg_color": "gray",
            "font_color": "white",
            "bold": True
        })


        # On injecte la ligne de titre dans la première feuille    
        worksheet.write("A1", "REFERENCE", header_style)
        worksheet.write("B1", "TYPE", header_style)
        worksheet.write("C1", "COMMENTAIRE", header_style)
        worksheet.write("D1", "PRIX", header_style)
        worksheet.write("E1", "ACTION", header_style)

        pos = 1
        derniereLigne = pos + len(catalogue)

        for point in catalogue:
            pos = pos + 1
            style = workbook.add_format({
                "bg_color": "white",
                "font_color": "black",
                "bold": False
            })
   
            worksheet.write("A"+str(pos), point.Reference, style)
            worksheet.write("B"+str(pos), point.type, style)
            worksheet.write("C"+str(pos), point.comment, style)
            worksheet.write("D"+str(pos), point.price, style)
            worksheet.write("E"+str(pos), "", style)


    message = "Catalogue générée"
    return message




#Page Download Catalogue
def download_catalogue(request, filename, newName):
    # Define the full file path
    filepath = MEDIA_URL + filename
    # Open the file for reading content
    with open(filepath, 'rb') as f:
        data = f.read()
   
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    name = newName + ".xlsx"
    # Set the return value of the HttpResponse
    response = HttpResponse(data, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % name
    # Return the response value
    return response


# def listPack(request):
#     message = ''

#     packsIOTUnit = PackIOTUnit.objects.all()

#     packUPDATE_ref = ""


#     if request.method == "POST":
#         #PACKS IOT
#         if(request.POST.get("form_type") == "PackIOTAddform"):
#             if request.POST.get("Add") != None:
#                 if not PackIOTUnit.objects.filter(Reference=request.POST.get('referenceIOT_Add')).exists():
#                     packsIOTUnit.create(Reference = request.POST.get('referenceIOT_Add'), 
#                         type = request.POST.get('typeIOT_Add'), 
#                         comment = request.POST.get('commentIOT_Add'), 
#                         price=request.POST.get('priceIOT_Add'))
#                 else:
#                     message = "pack existant"
#         elif (request.POST.get("form_type") == "PackIOTSuppform"):
#             packdel = packsOPT.get(Reference=request.POST.get('Supp'))
#             packdel.delete()

#         if(request.POST.get("form_type") == "PackIOTModifform"):
#             if request.POST.get("Modif") != None:
#                 packUPDATE_ref = request.POST.get("Modif")
#         elif(request.POST.get("form_type") == "PackIOTUPGform"):   
#             if request.POST.get("ValidModif") != None:
#                 print(request.POST.get("ValidModif"))
#                 PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(type=request.POST.get('typeIOT_Upd'))
#                 PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(comment=request.POST.get('commentIOT_Upd'))
#                 PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(price=float(request.POST.get('priceIOT_Upd').replace(",",".")))
#                 PackIOTUnit.objects.filter(Reference=request.POST.get("ValidModif")).update(Reference=request.POST.get('reference_Upd'))


#     return render(request, 'polls/packs.html', {
#         'message': message,
#         'packsTG': packsTG,
#         'packsOPT': packsOPT,
#         'packsIOTUnit': packsIOTUnit,
#         'packUPDATE' : packUPDATE_ref,
#         })

