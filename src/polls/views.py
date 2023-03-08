from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

from .models import Chaufferie

#Page 1: Choix de la configuration
def IndexView(request):
    return render(request, 'polls/index.html')

#Page 2: Définition de la configuration de la chaufferie
def ChaufferieView(request):
    chaufferie = get_object_or_404(Chaufferie)
    return render(request, 'polls/chaufferie.html', {'chaufferie': chaufferie})
