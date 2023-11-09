from django.forms import CharField, IntegerField
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.Typology.modelsEquip import LotIOT, Point
from ..models.Typology.modelsChaudiere import Chaufferie
from math import *
from ..models.Pack.modelsAutom import Automate, Prestation
from django.db.models import Q
from ..configAutom.configWIT import configWIT
from ..configAutom.configDISTECH import configDISTECH

from ..configAutom.configPROG import configPROG

class packValide():
    Reference: CharField(max_length=200)
    AIreserve:IntegerField() 
    DIreserve:IntegerField() 
    AOreserve:IntegerField() 
    DOreserve:IntegerField() 

def newConfig(request):
    message = ""

    # Détermination du pack de TELEGESTION
    if len(Point.objects.filter(user=request.user.username))>1:
        
        nbAI = Point.objects.filter(user=request.user.username, type='TOTAL').values('TM')[0]['TM']
        nbDI = Point.objects.filter(user=request.user.username, type='TOTAL').values('TS')[0]['TS']
        nbAO = Point.objects.filter(user=request.user.username, type='TOTAL').values('TR')[0]['TR']
        nbDO = Point.objects.filter(user=request.user.username, type='TOTAL').values('TC')[0]['TC']

        liste = Point.objects.filter(user=request.user.username)
        nbMbus = 0
        nbModbus = 0
        for p in liste:
            if p.equip == "Compteurs" and p.Mbus > 0:
                nbMbus += 1
            if p.equip == "Compteurs" and p.Modbus > 0:
                nbModbus += 1 

        # Dimensionnement d'un automate si aucun pack existant
        c = Chaufferie.objects.get(user=request.user.username)
        configWIT(request, request.user.username, c.modemNec, nbMbus)
        configDISTECH(request, request.user.username, c.modemNec, c.nbPortModem, nbMbus)
        configPROG(request, request.user.username)


        automate = Automate.objects.filter(user=request.user.username, marque='WIT')

    prestationPrix = Prestation.objects.filter(user=request.user.username).values('coutToT')[0]['coutToT']

    automateWIT = Automate.objects.filter(user=request.user.username, marque='WIT')
    automatePrixWIT = Automate.objects.filter(user=request.user.username, marque='WIT').values('cout')[0]['cout']
    coutTotalWIT = round(automatePrixWIT + prestationPrix, 2)
    automateDISTECH = Automate.objects.filter(Q(user=request.user.username) & (Q(marque="DISTECH") | Q(type="MODEM")))
    automatePrixDISTECH = Automate.objects.filter(Q(user=request.user.username) & (Q(marque="DISTECH") | Q(type="MODEM"))).values('cout')[0]['cout']
    coutTotalDISTECH = round(automatePrixDISTECH + prestationPrix, 2)

    return render(request, 'polls/configAutomate.html', {
        'message': message,
        'automateWIT': automateWIT,
        'automatePrixWIT' : automatePrixWIT,
        'coutTotalWIT': coutTotalWIT,
        'automateDISTECH': automateDISTECH,
        'automatePrixDISTECH' : automatePrixDISTECH,
        'coutTotalDISTECH': coutTotalDISTECH,
        'PrestationPrix' : prestationPrix,
        })
