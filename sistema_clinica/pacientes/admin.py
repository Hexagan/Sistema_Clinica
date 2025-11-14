from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "dni", "telefono", "usuario")
    search_fields = ("nombre", "apellido", "dni")
    list_filter = ("usuario",)
    ordering = ("apellido", "nombre")
