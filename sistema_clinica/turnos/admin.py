from django.contrib import admin
from .models import Turno

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "profesional", "fecha", "hora", "estado")
    search_fields = ("paciente__nombre", "paciente__apellido", "profesional__apellido")
    list_filter = ("estado", "profesional")
    ordering = ("fecha", "hora")
