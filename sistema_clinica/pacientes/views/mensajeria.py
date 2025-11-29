# pacientes/views/mensajeria.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from pacientes.mixins import PacienteAccessMixin
from pacientes.models import Mensaje
from profesionales.models import Profesional


class MensajeriaView(PacienteAccessMixin, View):
    template_name = "pacientes/mensajeria.html"

    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        mensajes = Mensaje.objects.filter(
            remitente=request.user
        ).order_by("-creado")

        return render(request, self.template_name, {
            "paciente": paciente,
            "paciente_id": paciente.id,
            "mensajes": mensajes,
        })


class NuevoMensajeView(PacienteAccessMixin, View):
    template_name = "pacientes/nuevo_mensaje.html"

    def get(self, request, paciente_id):
        paciente = self.get_paciente()
        profesionales = Profesional.objects.filter(estado=True).order_by("nombre")

        pre = request.GET.get("prof")
        prof_pre = int(pre) if pre and pre.isdigit() else None

        return render(request, self.template_name, {
            "paciente": paciente,
            "paciente_id": paciente.id,
            "profesionales": profesionales,
            "prof_preseleccionado": prof_pre,
        })

    def post(self, request, paciente_id):
        profesional_id = request.POST.get("profesional")
        texto = request.POST.get("texto", "").strip()

        if profesional_id and texto:
            prof = get_object_or_404(Profesional, id=profesional_id)
            Mensaje.objects.create(
                remitente=request.user,
                profesional_destino=prof,
                texto=texto
            )
        return redirect("pacientes:mensajeria", paciente_id=paciente_id)


class MensajeDetalleView(PacienteAccessMixin, View):
    def get(self, request, paciente_id, mensaje_id):
        paciente = self.get_paciente()
        mensaje = get_object_or_404(Mensaje, id=mensaje_id, remitente=request.user)

        if not mensaje.leido:
            mensaje.leido = True
            mensaje.save()

        return render(request, "pacientes/mensaje_detalle.html", {
            "paciente": paciente,
            "paciente_id": paciente_id,
            "mensaje": mensaje,
        })
