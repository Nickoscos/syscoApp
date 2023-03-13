

#Création de la classe d'une donnée
dataPts = {
    'libelle': 'libellé',
    'TM': 0,
    'TS': 0,
    'TS imp':0,
    'TR': 0,
    'TC': 0
}


#Création des classes des équipements
# Pompe
class Pompe():
    defaut : dataPts
    commande : dataPts

    def __init__(self, nom):
        self.defaut = {
            'libelle': 'Défaut ' + nom,
            'TM': 0,
            'TS': 1,
            'TS imp':0,
            'TR': 0,
            'TC': 0
        }
        self.commande = {
            'libelle': 'Commande ' + nom,
            'TM': 0,
            'TS': 0,
            'TS imp':0,
            'TR': 0,
            'TC': 1
        }

# V2V
class V2V():
    fdc : dataPts
    commande : dataPts

    def __init__(self, nom):
        self.fdc = {
            'libelle': 'retour ouverture ' + nom,
            'TM': 0,
            'TS': 1,
            'TS imp':0,
            'TR': 0,
            'TC': 0
        }
        self.commande = {
            'libelle': 'Commande ouverture' + nom,
            'TM': 0,
            'TS': 0,
            'TS imp':0,
            'TR': 0,
            'TC': 1
        }
