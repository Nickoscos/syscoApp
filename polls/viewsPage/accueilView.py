from django.shortcuts import render
from django.shortcuts import redirect

def accueil(request):
    return render(request, 'polls/accueil.html', {})