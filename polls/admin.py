from django.contrib import admin

from .models.Typology.modelsChaudiere import Chaufferie
from .models.Typology.modelsEquip import Point
from .models.Pack.modelsPacks import listePacks

admin.site.register(Chaufferie)
admin.site.register(Point)
admin.site.register(listePacks)