from django.shortcuts import render, get_object_or_404, redirect
from .models import Turno
from profesionales.models import Especialidad, Profesional

def solicitar_turno(request):
    context = {
        "especialidades": Especialidad.objects.all(),
        "profesionales": Profesional.objects.all(),
    }
    return render(request, "turnos/solicitar_turno.html", context)


def turno_exitoso(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    return render(request, "turnos/turno_exitoso.html", {"turno": turno})


def historial_turnos(request):
    turnos = Turno.objects.filter(paciente=request.user).order_by("-fecha")
    return render(request, "turnos/historial_turnos.html", {"turnos": turnos})


def ver_turno(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    return render(request, "turnos/ver_turno.html", {"turno": turno})
