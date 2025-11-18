from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente
from .forms import PacienteCustomForm, RegistroCustomForm, LoginForm

# -----------------------------
# REGISTRO DE USUARIO
# -----------------------------


def login_usuario(request):
    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect("usuarios:perfil")
    return render(request, "usuarios/login.html", {"form": form})


def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroCustomForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Crear usuario
            usuario = User.objects.create_user(
                username=username,
                password=password
            )

            login(request, usuario)
            return redirect("usuarios:perfil")

    else:
        form = RegistroCustomForm()

    return render(request, "usuarios/registrar_custom.html", {"form": form})



# -----------------------------
# PERFIL DEL USUARIO
# -----------------------------
@login_required
def perfil_usuario(request):
    perfil = request.user.perfil
    pacientes = perfil.pacientes.all()
    return render(request, "usuarios/perfil.html", {
        "usuario": request.user,
        "pacientes": pacientes
    })


# -----------------------------
# DETALLE DE PACIENTE (solo si pertenece)
# -----------------------------
@login_required
def detalle_paciente_usuario(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if paciente not in request.user.perfil.pacientes.all():
        return render(request, "usuarios/acceso_denegado.html")

    return render(request, "usuarios/paciente_detalle.html", {"paciente": paciente})


# -----------------------------
# CREAR PACIENTE
# -----------------------------
@login_required
def crear_paciente(request):
    if request.method == "POST":
        form = PacienteCustomForm(request.POST)

        if form.is_valid():
            datos = form.cleaned_data

            paciente = Paciente.objects.create(
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                dni=datos["dni"],
                email=datos["email"],
                telefono=datos["telefono"],
                fecha_nacimiento=datos["fecha_nacimiento"],
                obra_social=datos["obra_social"],
            )

            request.user.perfil.pacientes.add(paciente)

            return redirect("usuarios:perfil")

    else:
        form = PacienteCustomForm()

    return render(request, "usuarios/crear_paciente.html", {"form": form})
