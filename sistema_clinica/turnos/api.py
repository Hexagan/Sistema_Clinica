import qrcode
import base64
from io import BytesIO
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Turno, Estado
from pacientes.models import Paciente
from profesionales.models import Profesional, Servicio

@csrf_exempt
def reservar_turno(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST requerido"}, status=400)

    data = request.POST

    fecha = data.get("fecha")
    hora = data.get("hora")
    paciente_id = data.get("paciente_id")
    profesional_id = data.get("profesional_id")
    servicio_id = data.get("servicio_id")
    modalidad = data.get("modalidad")  # PRES / TELE

    if not all([fecha, hora, paciente_id, profesional_id, servicio_id, modalidad]):
        return JsonResponse({"error": "Faltan parámetros"}, status=400)

    # Validar modalidad
    profesional = Profesional.objects.get(id=profesional_id)

    if profesional.tipo_consulta == "PRES" and modalidad != "PRES":
        return JsonResponse({"error": "El profesional solo atiende presencial"}, status=400)

    if profesional.tipo_consulta == "TELE" and modalidad != "TELE":
        return JsonResponse({"error": "El profesional solo atiende teleconsulta"}, status=400)

    # Validar turno libre
    if Turno.objects.filter(
        profesional_id=profesional_id,
        servicio_id=servicio_id,
        fecha=fecha,
        hora=hora
    ).exists():
        return JsonResponse({"error": "Turno ya reservado"}, status=409)

    estado_confirmado = Estado.objects.get(descripcion="Confirmado")

    turno = Turno.objects.create(
        paciente_id=paciente_id,
        profesional_id=profesional_id,
        servicio_id=servicio_id,
        fecha=fecha,
        hora=hora,
        estado=estado_confirmado,
        modalidad=modalidad
    )

    # Guardar solo texto QR (no base64 gigante)
    qr_text = f"TURNO-{turno.id}"
    turno.qr_code = qr_text
    turno.save()

    # Generar QR base64 para enviar al front (no guardar)
    img = qrcode.make(qr_text)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({
        "mensaje": "Turno reservado",
        "turno_id": turno.id,
        "qr": qr_base64
    })

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