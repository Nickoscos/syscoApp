from django.shortcuts import render


#Page 1: Choix de la configuration
def IndexView(request):
    return render(request, 'polls/index.html')
