import xlsxwriter
from ..models.Typology.modelsEquip import Point
from django.http import HttpResponse
import mimetypes
from DEFPTS.settings import MEDIA_URL
from django.http.response import HttpResponse
import pandas as pd


def generationXls(request, username):
    liste = Point.objects.filter(user=username)

    #Initialisation du message
    message = ""

    file = MEDIA_URL + "listedepoints.xlsx"

    # On crée un nouveau classeur
    with xlsxwriter.Workbook(file) as workbook:

        # On y ajoute une première feuille
        worksheet = workbook.add_worksheet("Liste")

        # On dimensionne les colonnes
        worksheet.set_column("A:A", 60)
        worksheet.set_column("B:B", 60)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 20)
        worksheet.set_column("G:G", 20)
        worksheet.set_column("H:H", 20)

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
        worksheet.write("A1", "Sous-ensemble", header_style)
        worksheet.write("B1", "Libellé", header_style)
        worksheet.write("C1", "Télé-Mesure", header_style)
        worksheet.write("D1", "Télé-Signalisation", header_style)
        worksheet.write("E1", "Télé-Réglage", header_style)
        worksheet.write("F1", "Télé-Commande", header_style)
        worksheet.write("G1", "Mbus", header_style)
        worksheet.write("H1", "Modbus", header_style)
        worksheet.write("I1", "", header_style)

        pos = 1
        derniereLigne = pos + len(liste)

        for point in liste:
            pos = pos + 1
            if pos == derniereLigne: 
                style = header_style
            else :
                style = point_style

            worksheet.write("A"+str(pos), point.equip, style)
            worksheet.write("B"+str(pos), point.libelle, style)
            worksheet.write("C"+str(pos), point.TM, style)
            worksheet.write("D"+str(pos), point.TS, style)
            worksheet.write("E"+str(pos), point.TR, style)
            worksheet.write("F"+str(pos), point.TC, style)
            worksheet.write("G"+str(pos), point.Mbus, style)
            worksheet.write("H"+str(pos), point.Modbus, style)
            worksheet.write("I"+str(pos), "", style)

    message = "Liste de points générée"
    return message
    
    

#Page Download LISTE DE POINTS
def download_file(request, filename, newName):
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

#Page Upload LISTE DE POINTS
def upload_file(request, file):
    fileexcel = pd.read_excel(file)  


    try:
        Point.objects.filter(user=request.user.username).delete()
        
    except Point.DoesNotExist:
        # listeNew = Point.objects.create(user=request.user.username)
        print("Liste non existante")

    print(fileexcel)
    listeNew = Point.objects.filter(user=request.user.username)
    for index, row in fileexcel.iterrows():
        print(str(row['Libellé']))
        if not('nan' in str(row['Libellé'])) and not('TOTAUX' in str(row['Libellé'])): 
            listeNew.create(
                        equip= row['Sous-ensemble'],
                        type= "",
                        libelle= row['Libellé'], 
                        TM= row['Télé-Mesure'], 
                        TS= row['Télé-Signalisation'], 
                        TR= row['Télé-Réglage'], 
                        TC= row['Télé-Commande'],
                        Mbus=0,
                        Modbus=0,
                        Supp=False,
                        user=request.user.username)
        

    # liste = Point.objects.filter(user=request.user.username)
    # for l in liste:
    #     print (l.equip + " " + l.libelle + " " + str(l.TM) + " " + str(l.TS) + " " + str(l.TR) + " " + str(l.TC))
    
    # listeNew = Point.objects.create(user=request.user.username)
    # listeNew.create(
    #             equip= gen.nomGen,
    #             type= 'Temp',
    #             libelle= 'Température extérieure ', 
    #             TM=1, 
    #             TS=0, 
    #             TR=0, 
    #             TC=0,
    #             Mbus=0,
    #             Modbus=0,
    #             Supp=False,
    #             user=username)


# class Point(models.Model):
#     equip = models.CharField(max_length=200, default='equipement')
#     libelle = models.CharField(max_length=200, default='libellé')
#     type = models.CharField(max_length=200, default='')
#     TM = models.IntegerField(default=0)
#     TS = models.IntegerField(default=0)
#     TR = models.IntegerField(default=0)
#     TC = models.IntegerField(default=0)
#     Mbus = models.IntegerField(default=0)
#     Modbus = models.IntegerField(default=0)
#     Supp = models.BooleanField(default=False)
#     user = models.CharField(max_length=200, default="")