import qrcode
import base64
from io import BytesIO
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Turno, Estado
from pacientes.models import Paciente
from profesionales.models import Profesional, Servicio

def api_profesional(request, profesional_id):
    try:
        prof = Profesional.objects.get(id=profesional_id)
        return JsonResponse({
            "id": prof.id,
            "nombre": prof.nombre,
            "tipo_consulta": prof.tipo_consulta,  # PRES, TELE, AMBOS
            "especialidad": prof.especialidad.id
        })
    except Profesional.DoesNotExist:
        return JsonResponse({"error": "No existe profesional"}, status=404)