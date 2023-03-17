from django.urls import path

from . import views
from .pages import ListePtsview

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView, name='index'),
    # ex: /polls/chaufferie/
    path('chaufferie/', ListePtsview.chaufferieView, name='chaufferie'),
]