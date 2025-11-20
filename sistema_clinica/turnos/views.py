from django.shortcuts import render, get_object_or_404, redirect
from .models import Turno, Estado
from profesionales.models import Especialidad, Profesional
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.contrib import messages
import json

# -----------------------------
# SOLICITAR TURNO
# -----------------------------

def solicitar_turno(request, paciente_id):
    perfil = request.user.perfil
    paciente = perfil.pacientes.get(pk=paciente_id)

    profesionales = Profesional.objects.all()

    profesionales_data = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "especialidad": p.especialidad.id,
            "modalidad": p.tipo_consulta,
        }
        for p in profesionales
    ]

    DIAS_SEMANA = [
        ("LUN", "Lun"),
        ("MAR", "Mar"),
        ("MIE", "Mié"),
        ("JUE", "Jue"),
        ("VIE", "Vie"),
        ("SAB", "Sáb"),
        ("DOM", "Dom"),
    ]

    context = {
        "paciente": paciente,
        "especialidades": Especialidad.objects.all(),
        "profesionales": profesionales,
        "profesionales_json": json.dumps(profesionales_data, cls=DjangoJSONEncoder),
        "dias_semana": DIAS_SEMANA,
    }

    return render(request, "turnos/solicitar_turno.html", context)


# -----------------------------
# TURNOS DISPONIBLES
# -----------------------------

def turnos_disponibles(request):
    especialidad = request.GET.get("especialidad")
    profesional_id = request.GET.get("profesional")
    modo = request.GET.get("modo")
    hora_desde = request.GET.get("hora_desde")
    hora_hasta = request.GET.get("hora_hasta")
    dias_preferidos = request.GET.getlist("dias[]")
    paciente_id = request.GET.get("paciente_id")

    # Estado PENDIENTE = disponible
    estado_disponible = Estado.objects.get(pk=1)

    turnos = Turno.objects.select_related(
        'profesional',
        'profesional__especialidad',
        'estado'
    ).filter(estado=estado_disponible)

    # Filtros directos
    if especialidad:
        turnos = turnos.filter(profesional__especialidad_id=especialidad)

    if profesional_id:
        turnos = turnos.filter(profesional_id=profesional_id)

    if modo:
        turnos = turnos.filter(profesional__tipo_consulta=modo)

    if hora_desde:
        turnos = turnos.filter(hora__gte=hora_desde)

    if hora_hasta:
        turnos = turnos.filter(hora__lte=hora_hasta)

    # Filtrar por días de semana
    if dias_preferidos:
        turnos = [
            t for t in turnos
            if any(d in t.profesional.dias_como_lista() for d in dias_preferidos)
        ]

    # ordenar
    turnos = sorted(turnos, key=lambda t: (t.fecha, t.hora))

    return render(request, "turnos/turnos_disponibles.html", {
        "turnos": turnos,
        "query": request.GET,
        "paciente_id": paciente_id,
    })


# -----------------------------
# RESERVAR TURNO
# -----------------------------

@transaction.atomic
def reservar_turno(request):

    if request.method != "POST":
        return redirect("turnos:solicitar_turno", paciente_id=request.POST.get("paciente_id") or "")

    turno_id = request.POST.get("turno_id")
    paciente_id = request.POST.get("paciente_id")

    estado_disponible = Estado.objects.get(pk=1)   # Pendiente
    estado_confirmado = Estado.objects.get(pk=2)   # Confirmado

    if not turno_id:
        messages.error(request, "No se seleccionó ningún turno.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    turno = Turno.objects.select_for_update().get(pk=turno_id)

    # sigue disponible?
    if turno.estado != estado_disponible:
        messages.error(request, "El turno ya fue reservado por otro paciente.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Asignar paciente
    from pacientes.models import Paciente
    paciente = Paciente.objects.get(pk=paciente_id)

    turno.paciente = paciente
    turno.estado = estado_confirmado
    turno.save()

    messages.success(request, f"Turno reservado correctamente.")
    return redirect("turnos:turno_exitoso", paciente_id=paciente.id, turno_id=turno.id)


# -----------------------------
# TURNOS VARIOS
# -----------------------------

def turno_exitoso(request, paciente_id, turno_id):
    perfil = request.user.perfil
    paciente = perfil.pacientes.get(pk=paciente_id)
    turno = get_object_or_404(Turno, id=turno_id, paciente=paciente)
    return render(request, "turnos/turno_exitoso.html", {"paciente": paciente, "turno": turno})


def historial_turnos(request, paciente_id):
    perfil = request.user.perfil
    paciente = perfil.pacientes.get(pk=paciente_id)
    turnos = Turno.objects.filter(paciente=paciente).order_by("-fecha")
    return render(request, "turnos/historial_turnos.html", {"paciente": paciente, "turnos": turnos})


def ver_turno(request, paciente_id, turno_id):
    perfil = request.user.perfil
    paciente = perfil.pacientes.get(pk=paciente_id)
    turno = get_object_or_404(Turno, id=turno_id, paciente=paciente)
    return render(request, "turnos/ver_turno.html", {"paciente": paciente, "turno": turno})
