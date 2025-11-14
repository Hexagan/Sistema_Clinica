from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("id", "numero_afiliado", "nombre", "apellido", "dni", "telefono", "perfil_usuario")
    search_fields = ("nombre", "apellido", "dni", "numero_afiliado")
    list_filter = ("perfil_usuario",)
    ordering = ("nombre",)
