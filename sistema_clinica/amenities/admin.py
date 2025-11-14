from django.contrib import admin
from .models import Amenity

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion", "precio")
    search_fields = ("nombre",)
    ordering = ("nombre",)
