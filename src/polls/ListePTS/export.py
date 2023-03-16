import xlsxwriter
from tkinter import filedialog
from tkinter import *

def generationXls(liste):

    Tk().withdraw()
    filename = filedialog.asksaveasfile(initialdir = "C:\\",title = "Select file", defaultextension=".xls") 
    print(filename)

    # On crée un nouveau classeur
    with xlsxwriter.Workbook("listedepoints.xlsx") as workbook:

        # On y ajoute une première feuille
        worksheet = workbook.add_worksheet("Liste")

        # On dimensionne les colonnes
        worksheet.set_column("A:A", 60)
        worksheet.set_column("B:B", 20)
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
        worksheet.write("A1", "Libellé", header_style)
        worksheet.write("B1", "Télé-Mesure", header_style)
        worksheet.write("C1", "Télé-Signalisation", header_style)
        worksheet.write("D1", "Télé-Réglage", header_style)
        worksheet.write("E1", "Télé-Commande", header_style)

        pos = 1
        derniereLigne = pos + len(liste.pts)

        for point in liste.pts:
            pos = pos + 1
            if pos == derniereLigne: 
                style = header_style
            else :
                style = point_style

            worksheet.write("A"+str(pos), point.libelle, style)
            worksheet.write("B"+str(pos), point.TM, style)
            worksheet.write("C"+str(pos), point.TS, style)
            worksheet.write("D"+str(pos), point.TR, style)
            worksheet.write("E"+str(pos), point.TC, style)

        
            