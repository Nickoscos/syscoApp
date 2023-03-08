from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView, name='index'),
    # ex: /polls/chaufferie/
    path('chaufferie/', views.ChaufferieView, name='chaufferie'),
]