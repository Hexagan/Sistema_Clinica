from django.shortcuts import render, redirect, get_object_or_404
from .forms import SolicitarTurnoForm
from pacientes.models import Paciente
from turnos.models import Turno, Estado

def solicitar_turno(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = SolicitarTurnoForm(request.POST)
        if form.is_valid():
            estado_reservado = Estado.objects.get(descripcion="Reservado")
            Turno.objects.create(
                paciente=paciente,
                profesional=form.cleaned_data['profesional'],
                servicio=form.cleaned_data['servicio'],
                estado=estado_reservado,
                fecha=form.cleaned_data['fecha'],
                hora=form.cleaned_data['hora'],
                observaciones=form.cleaned_data['observaciones']
            )
            return redirect('turno_exitoso')
    else:
        form = SolicitarTurnoForm()
    return render(request, 'usuarios/solicitar_turno.html', {'form': form, 'paciente': paciente})

def turno_exitoso(request):
    return render(request, 'usuarios/turno_exitoso.html')

def lista_turnos(request):
    # lógica para mostrar los turnos
    pass