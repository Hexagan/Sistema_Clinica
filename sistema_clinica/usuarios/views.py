from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente
from .forms import PacienteCustomForm
from pacientes.models import Paciente
from django.contrib.auth.decorators import login_required

def registrar_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("usuarios:perfil")
    else:
        form = UserCreationForm()

    return render(request, "usuarios/registrar.html", {"form": form})


def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect("usuarios:perfil")
    else:
        form = AuthenticationForm()

    return render(request, "usuarios/login.html", {"form": form})


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect("usuarios:login")


@login_required
def perfil_usuario(request):
    perfil = request.user.perfil
    pacientes = perfil.pacientes.all()
    return render(request, "usuarios/perfil.html", {
        "usuario": request.user,
        "pacientes": pacientes
    })


# --------------------------------------
# 🔒 RESTRICCIÓN DE ACCESO
# Solo puede ver un paciente si le pertenece al usuario logueado
# --------------------------------------
@login_required
def detalle_paciente_usuario(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    # Validar si pertenece
    if paciente not in request.user.perfil.pacientes.all():
        return render(request, "usuarios/acceso_denegado.html")

    return render(request, "usuarios/paciente_detalle.html", {"paciente": paciente})

@login_required
def crear_paciente(request):
    if request.method == "POST":
        form = PacienteCustomForm(request.POST)

        if form.is_valid():
            datos = form.cleaned_data

            # Crear el paciente
            paciente = Paciente.objects.create(
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                dni=datos["dni"],
                email=datos["email"],
                telefono=datos["telefono"],
                fecha_nacimiento=datos["fecha_nacimiento"],
                obra_social=datos["obra_social"],
                numero_afiliado=None  # Django lo autogenera si es AutoField
            )

            # Asociarlo al usuario logeado
            request.user.perfil.pacientes.add(paciente)

            return redirect("usuarios:perfil")

    else:
        form = PacienteCustomForm()

    return render(request, "usuarios/crear_paciente.html", {"form": form})
