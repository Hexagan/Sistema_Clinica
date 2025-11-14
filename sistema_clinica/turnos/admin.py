from django.contrib import admin
from .models import Turno

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "paciente",
        "profesional",
        "servicio",
        "estado",
        "fecha",
        "hora",
        "piso",
    )
    search_fields = (
        "paciente__nombre",
        "profesional__nombre",
        "servicio__nombre",
    )
    list_filter = ("fecha", "profesional", "estado")
    ordering = ("fecha", "hora")

