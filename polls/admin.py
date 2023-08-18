from django.contrib import admin

from .models.Typology.modelsChaudiere import Chaufferie
from .models.Pack.modelsPacks import listePacks

admin.site.register(Chaufferie)
admin.site.register(listePacks)