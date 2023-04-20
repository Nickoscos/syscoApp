from django.urls import path

from . import views
from .viewsPage import listeView

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', listeView.genListeView, name='chaufferie'),
    path('liste/', listeView.listePts, name='listePts'),

]