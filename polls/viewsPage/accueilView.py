from django.shortcuts import render
from django.shortcuts import redirect

def accueil(request):
    if request.user.is_authenticated :
        return render(request, 'polls/accueil.html', {})
    else :
        return render(request, 'registration/login.html', {})