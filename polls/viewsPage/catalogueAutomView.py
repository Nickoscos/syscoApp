from datetime import datetime
from django.shortcuts import redirect, render
import pandas as pd
from ..models.Pack.modelsAutom import carteAutom
from DEFPTS.settings import MEDIA_URL
import mimetypes
from django.http import HttpResponse
import xlsxwriter

def catalogueAutom(request):
    message = ''

    cartes = carteAutom.objects.all()


    carteUPDATE_ref = ""
    if request.method == "POST":
        #Catalogue automate
        if(request.POST.get("form_type") == "catalogueAddform"):
            if request.POST.get("Add") != None:
                if not carteAutom.objects.filter(reference=request.POST.get('reference_Add')).exists():
                    cartes.create( type = request.POST.get('type_Add'),
                        marque = request.POST.get('marque_Add'), 
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
        elif(request.POST.get("form_type") == "catalogueSuppform"):           
            if request.POST.get("Supp") != None:
                cartedel = cartes.get(reference=request.POST.get('Supp'))
                cartedel.delete()
        
        if(request.POST.get("form_type") == "catalogueModifform"):    
            print("Modif en cours")
            if request.POST.get("Modif") != None:
                carteUPDATE_ref = request.POST.get("Modif")
                print(carteUPDATE_ref)
        elif(request.POST.get("form_type") == "catalogueUPGform"):   
            if request.POST.get("ValidModif") != None:
                print(request.POST.get("ValidModif"))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(type=request.POST.get('type_Upd'))
                carteAutom.objects.filter(reference=request.POST.get("ValidModif")).update(marque=request.POST.get('marque_Upd'))
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

        # Soumission du formulaire de téléchargement catalogue
        elif (request.POST.get("form_type") == "exportCatalogue"):
            message = catalogueXls(request, request.user.username)
            fileName = "catalogueAutomate" + str(datetime.now() )
            return redirect("polls:exportcatalogAutom", filename="catalogueAutom.xlsx", newName=fileName)
        
        # Soumission du formulaire de chargement catalogue
        elif (request.POST.get("form_type") == "importCatalogue"): 
            file = request.FILES['myfile']
            print("chargement du catalogue ", file.name)
            upload_catalogue(request, file)

    return render(request, 'polls/catalogueAutomate.html', {
        'message': message,
        'catalogue': cartes,
        'itemUPDATE': carteUPDATE_ref,
        })

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
        
def catalogueXls(request, username):
    catalogue = carteAutom.objects.all()

    #Initialisation du message
    message = ""

    file = MEDIA_URL + "catalogueAutom.xlsx"

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
        worksheet.set_column("K:K", 20)
        worksheet.set_column("L:L", 20)
        worksheet.set_column("M:M", 20)
        worksheet.set_column("N:N", 20)
        worksheet.set_column("O:O", 20)
        worksheet.set_column("P:P", 20)
        worksheet.set_column("Q:Q", 20)
        worksheet.set_column("R:R", 20)
        worksheet.set_column("S:S", 20)
        worksheet.set_column("T:T", 20)
        worksheet.set_column("U:U", 20)

        # On définit un style qui sera utilisé pour la ligne de titre.
        # Pour obtenir toutes les caractéristiques disponibles : print(dir(header_style))
        header_style = workbook.add_format({
            "bg_color": "gray",
            "font_color": "white",
            "bold": True
        })

        point_style = workbook.add_format({
            "bg_color": "white",
            "font_color": "black",
            "bold": False
        })

        # On injecte la ligne de titre dans la première feuille    
        worksheet.write("A1", "TYPE", header_style)
        worksheet.write("B1", "MARQUE", header_style)
        worksheet.write("C1", "DENOMINATION", header_style)
        worksheet.write("D1", "DI", header_style)
        worksheet.write("E1", "DO", header_style)
        worksheet.write("F1", "AI", header_style)
        worksheet.write("G1", "AO", header_style)
        worksheet.write("H1", "UI", header_style)
        worksheet.write("I1", "UO", header_style)
        worksheet.write("J1", "DOR", header_style)
        worksheet.write("K1", "DO_UO", header_style)
        worksheet.write("L1", "nbEmpl", header_style)
        worksheet.write("M1", "extension", header_style)
        worksheet.write("N1", "rs232", header_style)
        worksheet.write("O1", "rs485", header_style)
        worksheet.write("P1", "ressources", header_style)
        worksheet.write("Q1", "maxModbus", header_style)
        worksheet.write("R1", "Imagerie", header_style)
        worksheet.write("S1", "maxMbus", header_style)
        worksheet.write("T1", "prix", header_style)
        worksheet.write("U1", "ACTION", header_style)

        pos = 1
        derniereLigne = pos + len(catalogue)

        for point in catalogue:
            pos = pos + 1
            style = header_style


            worksheet.write("A"+str(pos), point.type, style)
            worksheet.write("B"+str(pos), point.marque, style)
            worksheet.write("C"+str(pos), point.reference, style)
            worksheet.write("D"+str(pos), point.DI, style)
            worksheet.write("E"+str(pos), point.DO, style)
            worksheet.write("F"+str(pos), point.AI, style)
            worksheet.write("G"+str(pos), point.AO, style)
            worksheet.write("H"+str(pos), point.UI, style)
            worksheet.write("I"+str(pos), point.UO, style)
            worksheet.write("J"+str(pos), point.DOR, style)
            worksheet.write("K"+str(pos), point.DO_UO, style)
            worksheet.write("L"+str(pos), point.nbEmpl, style)
            worksheet.write("M"+str(pos), point.extension, style)
            worksheet.write("N"+str(pos), point.rs232, style)
            worksheet.write("O"+str(pos), point.rs485, style)
            worksheet.write("P"+str(pos), point.ressources, style)
            worksheet.write("Q"+str(pos), point.maxModbus, style)
            worksheet.write("R"+str(pos), point.Imagerie, style)
            worksheet.write("S"+str(pos), point.maxMbus, style)
            worksheet.write("T"+str(pos), point.prix, style)
            worksheet.write("U"+str(pos), "", style)

    message = "Catalogue générée"
    return message
    
#Page Upload LISTE DE POINTS
def upload_catalogue(request, file):
    print(file.name)
    fileexcel = pd.read_excel(file, sheet_name='Liste')  

    try:
        carteAutom.objects.all().delete()
        
    except carteAutom.DoesNotExist:
        print("Catalogue vide")

    print(len(fileexcel))
    catalogue = carteAutom.objects.all()
    for index, row in fileexcel.iterrows():
        print(str(row['DENOMINATION']))
        if not('nan' in str(row['DENOMINATION'])): 
            catalogue.create(
                        type= row['TYPE'],
                        marque= row['MARQUE'],
                        reference= row['DENOMINATION'], 
                        DI= row['DI'], 
                        DO= row['DO'], 
                        AI= row['AI'], 
                        AO= row['AO'],
                        UI= row['UI'],
                        UO= row['UO'],
                        DOR= row['DOR'],
                        DO_UO= row['DO_UO'],
                        nbEmpl= row['nbEmpl'], 
                        extension= row['extension'], 
                        rs232= row['rs232'], 
                        rs485= row['rs485'],
                        ressources= row['ressources'],
                        maxModbus= row['maxModbus'],
                        Imagerie= row['Imagerie'],
                        maxMbus= row['maxMbus'],
                        prix= row['prix'])    
