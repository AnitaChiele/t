from django.contrib import admin
from .models import Pais, UF, Cidade

admin.site.register(Pais)
admin.site.register(UF)
admin.site.register(Cidade)
