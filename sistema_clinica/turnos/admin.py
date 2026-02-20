from django.contrib import admin
from .models import Turno, Estado

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion")
    search_fields = ("descripcion",)

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "paciente",
        "profesional",
        "estado",
        "fecha",
        "hora",
        "modalidad",
    )
    search_fields = (
        "paciente__nombre",
        "profesional__nombre",
        "id",
    )
    list_filter = ("fecha", "profesional", "estado")
    ordering = ("fecha", "hora")

