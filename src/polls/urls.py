from django.urls import path

from . import views
from .viewsPage import ListePtsview

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', ListePtsview.chaufferieView, name='chaufferie'),
    # path('', views.IndexView, name='index'),
    # ex: /polls/chaufferie/
    #path('chaufferie/', ListePtsview.chaufferieView, name='chaufferie'),
]