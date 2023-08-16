from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .viewsPage import listeView
from .ListePTS import export

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', listeView.genListeView, name='chaufferie'),
    path('liste/', listeView.listePts, name='listePts'),
    path('downloadfile/<str:filename>', export.download_file, name='downloadfile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)