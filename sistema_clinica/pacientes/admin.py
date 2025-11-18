from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "dni", "telefono", "perfil_usuario")
    search_fields = ("nombre", "apellido", "dni")
    list_filter = ("perfil_usuario",)
    ordering = ("nombre",)

