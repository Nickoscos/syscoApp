import xlsxwriter
from django.http import HttpResponse
import mimetypes
import os
from DEFPTS.settings import MEDIA_URL
from django.http.response import HttpResponse

def generationXls(request, liste):
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
        worksheet.write("G1", "", header_style)

        pos = 1
        derniereLigne = pos + len(liste.pts)

        for point in liste.pts:
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
            worksheet.write("G"+str(pos), "", style)

    message = "Liste de points générée"
    return message

#Page Download LISTE DE POINTS
def download_file(request, filename):
    # Define the full file path
    filepath = MEDIA_URL + filename
    # Open the file for reading content
    with open(filepath, 'rb') as f:
        data = f.read()
   
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    name = "test.xlsx"
    # Set the return value of the HttpResponse
    response = HttpResponse(data, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % name
    # Return the response value
    return response