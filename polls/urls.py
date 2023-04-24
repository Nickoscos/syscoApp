from django.urls import path

from .viewsPage import listeView


app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', listeView.genListeView, name='chaufferie'),
    path('liste/', listeView.listePts, name='listePts'),
]