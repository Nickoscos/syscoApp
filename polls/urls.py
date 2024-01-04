from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .viewsPage import listeView, packsView, configView, catalogueAutomView, configAutomateView, accueilView
from .ListePTS import export


app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('accueil', accueilView.accueil, name='accueil'),
    path('', listeView.genListeView, name='chaufferie'),
    path('liste/', listeView.listePts, name='listePts'),
    path('downloadfile/<str:filename>/<str:newName>', export.download_file, name='downloadfile'),
    path('packs/', packsView.listPack, name='packsView'),
    path('catalogueAutom', catalogueAutomView.catalogueAutom, name='catalogueAutomView'),
    path('config/', configView.newConfig, name='config'),
    path('configAutomate/', configAutomateView.newConfig, name='configAutomate'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
