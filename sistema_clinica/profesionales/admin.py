from django.contrib import admin
from .models import Profesional

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "especialidad")
    search_fields = ("nombre", "apellido", "especialidad")
    list_filter = ("especialidad",)
    ordering = ("apellido", "nombre")
