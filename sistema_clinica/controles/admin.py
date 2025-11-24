from django.contrib import admin
from .models import (
    PesoAltura,
    Temperatura,
    FrecuenciaCardiaca,
    PresionArterial,
    Glucemia,
    FrecuenciaRespiratoria,
    Disnea,
    SaturacionOxigeno,
    Indicaciones,
)

class PacienteBaseAdmin(admin.ModelAdmin):
    """Admin genérico para modelos que tienen paciente."""
    list_filter = ("paciente", "fecha")
    search_fields = ("paciente__nombre", "paciente__apellido")


@admin.register(PesoAltura)
class PesoAlturaAdmin(PacienteBaseAdmin):
    list_display = ("id", "paciente", "altura", "peso", "imc", "fecha")
    ordering = ("-fecha",)

@admin.register(Temperatura)
class TemperaturaAdmin(PacienteBaseAdmin):
    list_display = ("id", "paciente", "valor", "zona", "fecha", "hora")
    ordering = ("-fecha", "-hora")

@admin.register(FrecuenciaCardiaca)
class FrecuenciaCardiacaAdmin(PacienteBaseAdmin):
    list_display = ("id", "paciente", "valor", "metodo", "fecha", "hora")
    ordering = ("-fecha", "-hora")

@admin.register(PresionArterial)
class PresionArterialAdmin(PacienteBaseAdmin):
    list_display = ("id", "paciente", "alta", "baja", "zona",
                    "tensiometro", "tomado_por", "fecha", "hora")
    ordering = ("-fecha", "-hora")

@admin.register(Glucemia)
class GlucemiaAdmin(PacienteBaseAdmin):
    list_display = ("id", "paciente", "valor", "post_comida", "fecha", "hora")
    ordering = ("-fecha", "-hora")

@admin.register(FrecuenciaRespiratoria)
class FrecuenciaRespiratoriaAdmin(PacienteBaseAdmin):
    list_display = ("id", "paciente", "valor", "fecha", "hora")
    ordering = ("-fecha", "-hora")

@admin.register(Disnea)
class DisneaAdmin(PacienteBaseAdmin):
    list_display = ("id", "paciente", "valor", "fecha", "hora")
    ordering = ("-fecha", "-hora")

@admin.register(SaturacionOxigeno)
class SaturacionOxigenoAdmin(PacienteBaseAdmin):
    list_display = ("id", "paciente", "valor", "oxigeno_suplementario", "fecha", "hora", "creado")
    ordering = ("-fecha", "-hora")

@admin.register(Indicaciones)
class IndicacionesAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "fecha", "activo")
    list_filter = ("activo", "fecha")
    search_fields = ("titulo", "descripcion")
    ordering = ("-fecha",)
