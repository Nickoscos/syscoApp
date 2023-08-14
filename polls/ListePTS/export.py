from mimetypes import MimeTypes
import xlsxwriter
from tkinter.filedialog import asksaveasfile
from tkinter import *
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect

def generationXls(request, liste):
    #Initialisation du message
    message = ""

    file = "listedepoints.xlsx"

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

    return redirect("polls:downloadListe")

    # message = "Liste de points générée"

    # return message

def download(request):
    # file = open('listedepoints.xlsx', 'rb')
    # filepath = 'listedepoints.xlsx'
    # path = open(filepath, 'r')
    # mime_type, _ = MimeTypes.guess_type(filepath)
    # response = HttpResponse(path, content_type=mime_type)
    # response['Content-Disposition'] = "attachment; filename=%s" % 'listedepoints.xlsx'
    # return response
    message = "download"
    return message
# def generationXls(liste):
#     #Initialisation du message
#     message = ""

#     #Gestion de la box pour enregistrer le fichier
#     root = Tk() #Ajout du widget tkinter
#     root.withdraw() #Séparer la box de la fenêtre de tkinter
#     root.attributes('-topmost', True)  # Affichage de la box au premier plan
#     root.iconify()  # Cache la fenetre de tkinter
#     files = [('Excel Document', '.xlsx'), ('All Files', '*.*')]
#     file = asksaveasfile(filetypes = files, defaultextension = files, parent=root) 
#     root.destroy() #Supprime le widget 
#     print(file.name)
#     if hasattr(file, 'name'):
#         # On crée un nouveau classeur
#         with xlsxwriter.Workbook(file.name) as workbook:

#             # On y ajoute une première feuille
#             worksheet = workbook.add_worksheet("Liste")

#             # On dimensionne les colonnes
#             worksheet.set_column("A:A", 60)
#             worksheet.set_column("B:B", 60)
#             worksheet.set_column("C:C", 20)
#             worksheet.set_column("D:D", 20)
#             worksheet.set_column("E:E", 20)
#             worksheet.set_column("F:F", 20)

#             # On définit un style qui sera utilisé pour la ligne de titre.
#             # Pour obtenir toutes les caractéristiques disponibles : print(dir(header_style))
#             header_style = workbook.add_format({
#                 "bg_color": "gray",
#                 "font_color": "white",
#                 "bold": True
#             })

#             point_style = workbook.add_format({
#                 "bg_color": "white",
#                 "font_color": "black",
#                 "bold": False
#             })

#             # On injecte la ligne de titre dans la première feuille    
#             worksheet.write("A1", "Sous-ensemble", header_style)
#             worksheet.write("B1", "Libellé", header_style)
#             worksheet.write("C1", "Télé-Mesure", header_style)
#             worksheet.write("D1", "Télé-Signalisation", header_style)
#             worksheet.write("E1", "Télé-Réglage", header_style)
#             worksheet.write("F1", "Télé-Commande", header_style)
#             worksheet.write("G1", "", header_style)

#             pos = 1
#             derniereLigne = pos + len(liste.pts)

#             for point in liste.pts:
#                 pos = pos + 1
#                 if pos == derniereLigne: 
#                     style = header_style
#                 else :
#                     style = point_style

#                 worksheet.write("A"+str(pos), point.equip, style)
#                 worksheet.write("B"+str(pos), point.libelle, style)
#                 worksheet.write("C"+str(pos), point.TM, style)
#                 worksheet.write("D"+str(pos), point.TS, style)
#                 worksheet.write("E"+str(pos), point.TR, style)
#                 worksheet.write("F"+str(pos), point.TC, style)
#                 worksheet.write("G"+str(pos), "", style)


#         message = "Liste de points générée"
#     else:
#         message = "Erreur lors de la génération de la liste de points, veuillez valider de nouveau le formulaire"

#     return message

        
            