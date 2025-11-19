from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Turno, Estado
from profesionales.models import Profesional
from servicios.models import Servicio
from datetime import datetime

@login_required
def solicitar_turno(request):

    if request.method == "POST":
        profesional = get_object_or_404(Profesional, id=request.POST["profesional"])
        servicio = get_object_or_404(Servicio, id=request.POST["servicio"])

        turno = Turno.objects.create(
            paciente=request.user.paciente,
            profesional=profesional,
            servicio=servicio,
            fecha=request.POST["fecha"],
            hora=request.POST["hora"],
            piso=request.POST["piso"],
            estado=Estado.objects.first(),
        )

        return render(request, "turno_exitoso.html", {"turno": turno})

    profesionales = Profesional.objects.all()
    servicios = Servicio.objects.all()

    return render(request, "solicitar_turno.html", {
        "profesionales": profesionales,
        "servicios": servicios
    })


@login_required
def historial_turnos(request):
    turnos = Turno.objects.filter(
        paciente=request.user.paciente
    ).order_by("-fecha", "-hora")

    return render(request, "historial_turnos.html", {"turnos": turnos})


@login_required
def ver_turno(request, turno_id):
    turno = get_object_or_404(
        Turno, id=turno_id, paciente=request.user.paciente
    )
    return render(request, "ver_turno.html", {"turno": turno})

@login_required
def turnos_agendados(request):
    turnos = Turno.objects.filter(
        paciente=request.user.paciente,
        fecha__gte=datetime.date.today()
    ).order_by("fecha", "hora")

    return render(request, "turnos_agendados.html", {"turnos": turnos})
