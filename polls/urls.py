from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .viewsPage import listeView


app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', listeView.genListeView, name='chaufferie'),
    path('liste/', listeView.listePts, name='listePts'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)