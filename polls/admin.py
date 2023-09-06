from django.contrib import admin

from .models.Typology.modelsChaudiere import Chaufferie
from .models.Typology.modelsEquip import Point
from .models.Pack.modelsPacks import PackTG, PackOPT, PackIOTUnit

admin.site.register(Chaufferie)
admin.site.register(Point)
admin.site.register(PackTG)
admin.site.register(PackOPT)
admin.site.register(PackIOTUnit)