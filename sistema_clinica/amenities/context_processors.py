from django.db.models import Count
from .models import BeneficioOtorgado

def beneficios_pendientes(request):
    if not request.user.is_authenticated:
        return {}

    perfil = getattr(request.user, "perfil", None)
    if not perfil:
        return {}

    paciente_id = request.session.get("paciente_id")
    if not paciente_id:
        return {}

    beneficios = (
        BeneficioOtorgado.objects
        .filter(paciente_id=paciente_id)
        .values("beneficio__amenity__nombre")
        .annotate(total=Count("id"))
    )

    # Normalizamos keys
    conteo = {
        item["beneficio__amenity__nombre"]: item["total"]
        for item in beneficios
    }

    beneficios_por_amenity = {
        "gimnasio": conteo.get("Gimnasio", 0),
        "nutricion": conteo.get("Relajación y Mindfulness", 0),
        "talleres": conteo.get("Talleres y Asesoramiento de Salud", 0),
        "kiosco": conteo.get("Kiosco y Nutrición", 0),
    }

    total_general = sum(beneficios_por_amenity.values())

    return {
        "beneficios_count": total_general,
        "beneficios_por_amenity": beneficios_por_amenity,
    }
