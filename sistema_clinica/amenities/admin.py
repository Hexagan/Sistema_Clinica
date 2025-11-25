from django.contrib import admin
from .models import Amenity, Beneficio, BeneficioOtorgado

class BenefitInline(admin.TabularInline):
    model = Beneficio
    extra = 0

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    inlines = [BenefitInline]

@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "amenity", "activo")
    list_filter = ("amenity", "activo")
    search_fields = ("titulo", "descripcion")

@admin.register(BeneficioOtorgado)
class BeneficioOtorgadoAdmin(admin.ModelAdmin):
    raw_id_fields = ("turno", "paciente", "beneficio")
    list_display = ("beneficio", "paciente", "turno", "timestamp", "notificado")
    list_filter = ("beneficio__amenity", "notificado")
    readonly_fields = ("timestamp",)
