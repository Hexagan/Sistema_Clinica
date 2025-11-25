from django.shortcuts import render, get_object_or_404
from pacientes.models import Paciente
from .models import Amenity, Beneficio, BeneficioOtorgado


def cargar_paciente(request, paciente_id):
    perfil = request.user.perfil
    return perfil.pacientes.get(pk=paciente_id)


def render_amenity(request, paciente_id, amenity_nombre, template_name):
    """Vista genérica para cualquier amenity."""

    paciente = cargar_paciente(request, paciente_id)

    # Obtener la amenity por nombre
    amenity = get_object_or_404(Amenity, nombre=amenity_nombre)

    # Beneficios activos
    beneficios = amenity.beneficios.filter(activo=True)

    # Beneficio otorgado para este amenity (si existe)
    beneficio_otorgado = (
        BeneficioOtorgado.objects.filter(
            paciente=paciente,
            beneficio__amenity=amenity
        )
        .select_related("beneficio")
        .first()
    )

    return render(request, template_name, {
        "paciente": paciente,
        "amenity": amenity,
        "beneficios": beneficios,
        "beneficio_otorgado": beneficio_otorgado,
    })


# ============================================================
# VISTAS ESPECÍFICAS
# ============================================================

def gimnasio(request, paciente_id):
    return render_amenity(
        request,
        paciente_id,
        "Gimnasio",
        "amenities/gimnasio.html"
    )


def kiosco(request, paciente_id):
    return render_amenity(
        request,
        paciente_id,
        "Kiosco y Nutrición",
        "amenities/kiosco.html"
    )


def nutricion(request, paciente_id):
    return render_amenity(
        request,
        paciente_id,
        "Relajación y Mindfulness",
        "amenities/nutricion.html"
    )


def talleres(request, paciente_id):
    return render_amenity(
        request,
        paciente_id,
        "Talleres y Asesoramiento de Salud",
        "amenities/talleres.html"
    )
