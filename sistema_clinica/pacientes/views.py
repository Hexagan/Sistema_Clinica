from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Paciente

@login_required
def portal_paciente(request):
    pacientes = Paciente.objects.all()
    especialidades = []  # Reemplazar con modelo
    return render(request, 'pacientes/portal_paciente.html', {
        'pacientes': pacientes,
        'especialidades': especialidades,
    })

@login_required
def crear_paciente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        obra_social = request.POST.get('obra_social')
        
        # Validación DNI duplicado
        if Paciente.objects.filter(dni=dni).exists():
            error = "Ya existe un paciente con ese DNI."
            return render(request, "pacientes/crear_paciente.html", {"error": error})

        # Crear el paciente con la FK correcta
        nuevo_paciente = Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            obra_social=obra_social,
            perfil_usuario=request.user.perfil   # ← FK obligatoria
        )
        
        # Asociarlo también al M2M
        request.user.perfil.pacientes.add(nuevo_paciente)

        return redirect('pacientes:creacion_paciente_exitosa')

    # GET → mostrar formulario
    return render(request, 'pacientes/crear_paciente.html')



@login_required
def creacion_paciente_exitosa(request):
    return render(request, 'pacientes/creacion_paciente_exitosa.html')


@login_required
def paciente_detalle(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    return render(request, 'pacientes/paciente_detalle.html', {'paciente': paciente})


@login_required
def ver_turnos(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    turnos = paciente.turno_set.all()
    return render(request, "turnos/ver_turnos.html", {
        "paciente": paciente,
        "turnos": turnos
    })

@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by("apellido", "nombre")
    return render(request, "pacientes/lista_pacientes.html", {
        "pacientes": pacientes
    })
