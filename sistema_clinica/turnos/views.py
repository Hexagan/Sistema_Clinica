from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from .models import Turno, Estado
from .forms import SolicitarTurnoForm
import uuid

# ----------- Solicitar turno -----------
def solicitar_turno(request):

    if request.method == "POST":
        form = SolicitarTurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)

            # Estado inicial: agendado
            estado_agendado = Estado.objects.get(descripcion="Agendado")
            turno.estado = estado_agendado

            # Generar QR único
            turno.qr_code = str(uuid.uuid4())

            turno.save()

            return redirect(reverse("turnos:turno_exitoso", args=[turno.id]))
    else:
        form = SolicitarTurnoForm()

    return render(request, "turnos/solicitar_turno.html", {"form": form})


# ----------- Turno exitoso -----------
def turno_exitoso(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    return render(request, "turnos/turno_exitoso.html", {"turno": turno})


# ----------- Ver turno -----------
def ver_turno(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    return render(request, "turnos/ver_turno.html", {"turno": turno})
