from django.shortcuts import render, get_object_or_404, redirect
from .models import Turno, Estado, Paciente
from collections import defaultdict
from profesionales.models import Especialidad, Profesional
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, time
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
    paciente = None
    paciente_id = request.GET.get("paciente_id")

    if paciente_id:
        paciente = request.user.perfil.pacientes.filter(pk=paciente_id).first()

    estado_disponible = Estado.objects.get(pk=1)

    # ==========================================
    # 1) CONSULTA BASE
    # ==========================================
    turnos = Turno.objects.select_related(
        "profesional",
        "profesional__especialidad",
        "estado"
    ).filter(estado=estado_disponible)

    
    # CONSULTA BASE
    turnos = Turno.objects.select_related(
        "profesional",
        "profesional__especialidad",
        "estado"
    ).filter(estado=estado_disponible)

    # FILTROS (solo queryset)
    if especialidad:
        turnos = turnos.filter(profesional__especialidad_id=especialidad)

    if profesional_id:
        turnos = turnos.filter(profesional_id=profesional_id)

    if modo == "PRES":
        turnos = turnos.filter(modalidad="PRES")

    elif modo == "TELE":
        turnos = turnos.filter(modalidad="TELE")

    if hora_desde:
        turnos = turnos.filter(hora__gte=hora_desde)

    if hora_hasta:
        turnos = turnos.filter(hora__lte=hora_hasta)


    print("Los dias preferidos son: ", dias_preferidos)
    # === FILTRO POR DÍAS PREFERIDOS ===
    dias_preferidos = request.GET.getlist("dias[]")

    if dias_preferidos:
        dias_preferidos = [d.upper() for d in dias_preferidos]

        MAP = {
            "Mon": "LUN",
            "Tue": "MAR",
            "Wed": "MIE",
            "Thu": "JUE",
            "Fri": "VIE",
            "Sat": "SAB",
            "Sun": "DOM",
        }

        turnos_filtrados = []
        for t in turnos:
            # Día real del turno (Mon/Tue/Wed…)
            dia_python = t.fecha.strftime("%a")

            # Convertirlo a español (LUN, MAR…)
            dia_turno = MAP[dia_python]

            # ¿Coincide con preferencias?
            if dia_turno in dias_preferidos:
                turnos_filtrados.append(t)

        turnos = turnos_filtrados

    # EXCLUIR TURNOS PASADOS
    from datetime import date, datetime
    hoy = date.today()
    ahora = datetime.now().time()

    turnos = [
        t for t in turnos
        if t.fecha > hoy or (t.fecha == hoy and t.hora > ahora)
    ]

    # ==========================================
    # 3) ORDEN
    # ==========================================
    turnos = sorted(turnos, key=lambda t: (t.fecha, t.hora))

    # ==========================================
    # 4) AGRUPAR POR FECHA
    # ==========================================
    turnos_por_dia = defaultdict(list)

    for turno in turnos:
        turnos_por_dia[turno.fecha].append(turno)

    fechas_ordenadas = sorted(turnos_por_dia.keys())

    # ==========================================
    # 5) ENVIAR AL TEMPLATE
    # ==========================================

    return render(request, "turnos/turnos_disponibles.html", {
        "paciente": paciente,
        "paciente_id": paciente_id,
        "fechas_ordenadas": fechas_ordenadas,
        "turnos_por_dia": turnos_por_dia,
        "query": request.GET,
    })

# -----------------------------
# RESERVAR TURNO
# -----------------------------

@transaction.atomic
def reservar_turno(request):
    # Solo POST permite reservar
    if request.method != "POST":
        # redirigir a donde vino o al portal si no hay referer
        return redirect(request.META.get("HTTP_REFERER", "/"))

    turno_id = request.POST.get("turno_id")
    paciente_id = request.POST.get("paciente_id")
    modo = request.POST.get("modo")  # "PRES" o "TELE"

    if not turno_id or not paciente_id:
        messages.error(request, "Faltan datos para reservar el turno.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Estados (asumo pk: 1 = Disponible, 2 = Confirmado)
    try:
        estado_disponible = Estado.objects.get(pk=1)
    except Estado.DoesNotExist:
        messages.error(request, "Estado 'Disponible' no configurado en la base.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    try:
        estado_confirmado = Estado.objects.get(pk=2)
    except Estado.DoesNotExist:
        messages.error(request, "Estado 'Confirmado' no configurado en la base.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Bloqueo optimista: obtener el turno con lock
    try:
        turno = Turno.objects.select_for_update().get(pk=turno_id)
    except Turno.DoesNotExist:
        messages.error(request, "El turno seleccionado no existe.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Verificar que el turno siga siendo disponible
    if turno.estado != estado_disponible:
        messages.error(request, "El turno ya fue reservado por otro paciente.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Validar paciente y que pertenezca al usuario
    try:
        paciente = Paciente.objects.get(pk=paciente_id)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente no encontrado.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Si tu flujo exige que el paciente pertenezca al perfil del usuario:
    if paciente not in request.user.perfil.pacientes.all():
        messages.error(request, "No tenés permiso para reservar turnos para ese paciente.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Validar modalidad recibida
    if modo not in ("PRES", "TELE"):
        messages.error(request, "Modalidad inválida.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Asignar paciente, estado y modalidad
    turno.paciente = paciente
    turno.estado = estado_confirmado
    turno.modalidad = modo
    turno.save()

    # Si el profesional es híbrido, bloquear/eliminar el turno espejo
    # (aquí lo marcamos como 'Confirmado' para que deje de aparecer como disponible)
    if turno.profesional.tipo_consulta == "AMBOS":
        Turno.objects.filter(
            profesional=turno.profesional,
            fecha=turno.fecha,
            hora=turno.hora
        ).exclude(id=turno.id).update(estado=estado_confirmado)

    messages.success(request, "Turno reservado correctamente.")

    # Redirigir a pantalla de éxito (ajusta nombres/args según tus urls)
    return redirect("turnos:turno_exitoso", paciente_id=paciente.id, turno_id=turno.id)


# -----------------------------
# TURNOS VARIOS
# -----------------------------

def turno_exitoso(request, paciente_id, turno_id):
    perfil = request.user.perfil
    paciente = perfil.pacientes.get(pk=paciente_id)
    turno = get_object_or_404(Turno, id=turno_id, paciente=paciente)
    return render(request, "turnos/turno_exitoso.html", {"paciente": paciente, "turno": turno})


def turnos_historial(request, paciente_id):
    perfil = request.user.perfil
    paciente = perfil.pacientes.get(pk=paciente_id)

    ahora = timezone.localtime()

    turnos = Turno.objects.filter(paciente=paciente)

    historial = []
    for t in turnos:
        dt = timezone.make_aware(datetime.combine(t.fecha, t.hora))

        # Atendido (3), Cancelado (5), o Confirmado pero vencido (2)
        if t.estado.pk in (3, 5) or (t.estado.pk == 2 and dt < ahora):
            historial.append(t)

    # Ordenar por fecha/hora descendente
    historial_ordenado = sorted(
        historial,
        key=lambda t: (t.fecha, t.hora),
    )

    return render(request, "turnos/turnos_historial.html", {
        "paciente": paciente,
        "turnos": historial_ordenado
    })


def turnos_agendados(request, paciente_id):
    perfil = request.user.perfil
    paciente = perfil.pacientes.get(pk=paciente_id)

    ahora = timezone.localtime()

    # Turnos cuyo estado es Confirmado y cuya fecha+hora es futura
    turnos = Turno.objects.filter(
        paciente=paciente,
        estado__pk=2  # Confirmado
    )

    turnos_futuros = []
    for t in turnos:
        dt = datetime.combine(t.fecha, t.hora)
        dt = timezone.make_aware(dt)
        if dt >= ahora:
            turnos_futuros.append(t)

    # ORDENAR MÁS RECIENTE → MÁS ANTIGUO
    turnos_ordenados = sorted(
        turnos_futuros,
        key=lambda t: (t.fecha, t.hora),
    )
    return render(request, "turnos/turnos_agendados.html", {
        "paciente": paciente,
        "turnos": turnos_ordenados
    })

def ver_turno(request, paciente_id, turno_id):
    perfil = request.user.perfil
    paciente = perfil.pacientes.get(pk=paciente_id)
    turno = get_object_or_404(Turno, id=turno_id, paciente=paciente)

    return render(request, "turnos/ver_turno.html", {
        "paciente": paciente,
        "turno": turno,
    })

def bloquear_turno_opuesto(self):
    from turnos.models import Turno

    opuesto = "PRES" if self.modalidad == "TELE" else "TELE"

    turno_opuesto = Turno.objects.filter(
        profesional=self.profesional,
        fecha=self.fecha,
        hora=self.hora,
        modalidad=opuesto,
        paciente__isnull=True  # debe ser turno plantilla
    ).first()

    if turno_opuesto:
        turno_opuesto.estado = "BLOQUEADO"
        turno_opuesto.save()

@transaction.atomic
def cancelar_turno(request, paciente_id, turno_id):
    perfil = request.user.perfil
    paciente = perfil.pacientes.get(pk=paciente_id)

    turno = get_object_or_404(Turno, pk=turno_id, paciente=paciente)

    if request.method != "POST":
        return redirect("turnos:turnos_agendados", paciente_id=paciente_id)

    estado_cancelado = Estado.objects.get(pk=5)  # Cancelado
    estado_disponible = Estado.objects.get(pk=1)  # Pendiente/Disponible

    # 1) El turno original pasa a CANCELADO
    turno.estado = estado_cancelado
    turno.save()

    # 2) Crear un nuevo turno disponible (plantilla)
    Turno.objects.create(
        profesional=turno.profesional,
        fecha=turno.fecha,
        hora=turno.hora,
        modalidad=turno.modalidad,  # ← conserva modalidad
        estado=estado_disponible,
        paciente=None
    )

    # 3) Si el profesional es híbrido, también recrear el turno espejo
    if turno.profesional.tipo_consulta == "AMBOS":
        modalidades = ["PRES", "TELE"]
        opuesta = "PRES" if turno.modalidad == "TELE" else "TELE"

        Turno.objects.create(
            profesional=turno.profesional,
            fecha=turno.fecha,
            hora=turno.hora,
            modalidad=opuesta,
            estado=estado_disponible,
            paciente=None
        )

    messages.success(request, "El turno fue cancelado correctamente.")
    return redirect("turnos:turnos_agendados", paciente_id=paciente_id)