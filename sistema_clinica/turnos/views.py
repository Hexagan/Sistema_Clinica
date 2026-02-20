import json, qrcode, base64, random

from io import BytesIO
from collections import defaultdict
from datetime import datetime, date

from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from .models import Turno, Estado
from pacientes.models import Paciente
from pacientes.mixins import PacienteAccessMixin
from profesionales.models import Especialidad, Profesional
from amenities.models import Beneficio, BeneficioOtorgado

class SolicitarTurnoView(LoginRequiredMixin, PacienteAccessMixin, TemplateView):
    template_name = "turnos/solicitar_turno.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = kwargs.get("paciente_id")
        paciente = self.get_paciente()

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

        context.update({
            "paciente": paciente,
            "especialidades": Especialidad.objects.all(),
            "profesionales": profesionales,
            "profesionales_json": json.dumps(profesionales_data, cls=DjangoJSONEncoder),
            "dias_semana": DIAS_SEMANA,
            "paciente_id": paciente_id,
        })
        return context


class TurnosDisponiblesView(LoginRequiredMixin, View):
    template_name = "turnos/turnos_disponibles.html"

    def _filtrar_por_dias(self, turnos, dias_preferidos):
        """Recibe iterable de turnos (queryset o list) y lista como ['LUN','MAR',...]"""
        if not dias_preferidos:
            return turnos

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

        filtrados = []
        for t in turnos:
            dia_python = t.fecha.strftime("%a")  # Mon/Tue...
            dia_turno = MAP.get(dia_python)
            if dia_turno and dia_turno in dias_preferidos:
                filtrados.append(t)
        return filtrados

    def get(self, request, *args, **kwargs):
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

        # base queryset
        qs = Turno.objects.select_related(
            "profesional",
            "profesional__especialidad",
            "estado"
        ).filter(estado=estado_disponible)

        # filtros queryset
        if especialidad:
            qs = qs.filter(profesional__especialidad_id=especialidad)
        if profesional_id:
            qs = qs.filter(profesional_id=profesional_id)
        if modo == "PRES":
            qs = qs.filter(modalidad="PRES")
        elif modo == "TELE":
            qs = qs.filter(modalidad="TELE")
        if hora_desde:
            qs = qs.filter(hora__gte=hora_desde)
        if hora_hasta:
            qs = qs.filter(hora__lte=hora_hasta)

        # El filtro usa python-dates, hay que convertir a lista para evitar problemas de queryset 
        turnos_list = list(qs)

        turnos_filtrados = self._filtrar_por_dias(turnos_list, dias_preferidos)

        # excluir turnos pasados (fecha/hora)
        hoy = date.today()
        ahora = datetime.now().time()
        turnos_future = [
            t for t in turnos_filtrados
            if t.fecha > hoy or (t.fecha == hoy and t.hora > ahora)
        ]

        # Buscar próximo turno futuro sin filtros restrictivos de fecha/hora/dias
        proximo_turno = None

        base_future = Turno.objects.filter(
            estado=estado_disponible,
            fecha__gte=date.today()
        ).select_related("profesional", "profesional__especialidad")

        if profesional_id:
            base_future = base_future.filter(profesional_id=profesional_id)
        elif especialidad:
            base_future = base_future.filter(profesional__especialidad_id=especialidad)

        if modo in ["PRES", "TELE"]:
            base_future = base_future.filter(modalidad=modo)

        proximo_turno = base_future.order_by("fecha", "hora").first()

        # ordenar y agrupar
        turnos_ordered = sorted(turnos_future, key=lambda t: (t.fecha, t.hora))
        turnos_por_dia = defaultdict(list)
        for turno in turnos_ordered:
            turnos_por_dia[turno.fecha].append(turno)
        fechas_ordenadas = sorted(turnos_por_dia.keys())

        hay_turnos = len(turnos_ordered) > 0

        return render(request, self.template_name, {
            "paciente": paciente,
            "paciente_id": paciente_id,
            "proximo_turno": proximo_turno,
            "fechas_ordenadas": fechas_ordenadas,
            "turnos_por_dia": turnos_por_dia,
            "query": request.GET,
            "hay_turnos": hay_turnos,
        })



class ReservarTurnoView(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        turno_id = request.POST.get("turno_id")
        paciente_id = request.POST.get("paciente_id")

        if not turno_id or not paciente_id:
            messages.error(request, "Faltan datos para reservar el turno.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        try:
            estado_disponible = Estado.objects.get(pk=1)
            estado_confirmado = Estado.objects.get(pk=2)
        except Estado.DoesNotExist:
            messages.error(request, "Estados no configurados correctamente.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        try:
            turno = Turno.objects.select_for_update().get(pk=turno_id)
        except Turno.DoesNotExist:
            messages.error(request, "El turno seleccionado no existe.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        if turno.estado != estado_disponible:
            messages.error(request, "El turno ya fue reservado por otro paciente.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        try:
            paciente = Paciente.objects.get(pk=paciente_id)
        except Paciente.DoesNotExist:
            messages.error(request, "Paciente no encontrado.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        if paciente not in request.user.perfil.pacientes.all():
            messages.error(request, "No tenés permiso para reservar turnos para ese paciente.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # asignar y guardar
        modo = turno.modalidad
        turno.paciente = paciente
        turno.estado = estado_confirmado
        turno.modalidad = modo
        turno.save()

        # generar QR y guardarlo base64
        qr_data = request.build_absolute_uri(
            reverse("turnos:checkin_qr") + f"?qr=TURNO:{turno.id};PACIENTE:{paciente.id};FECHA:{turno.fecha};HORA:{turno.hora}"
        )
        qr_img = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        turno.qr_code = base64.b64encode(buffer.getvalue()).decode()
        turno.save()

        # bloquear espejo si híbrido
        if turno.profesional.tipo_consulta == "AMBOS":
            Turno.objects.filter(
                profesional=turno.profesional,
                fecha=turno.fecha,
                hora=turno.hora
            ).exclude(id=turno.id).update(estado=estado_confirmado)

        messages.success(request, "Turno reservado correctamente.")
        return redirect("turnos:turno_exitoso", paciente_id=paciente.id, turno_id=turno.id)


class TurnoExitosoView(LoginRequiredMixin, PacienteAccessMixin, TemplateView):
    template_name = "turnos/turno_exitoso.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        turno_id = kwargs.get("turno_id")

        paciente = self.get_paciente()
        turno = get_object_or_404(Turno, id=turno_id, paciente=paciente)

        context.update({
            "paciente": paciente,
            "turno": turno,
        })
        return context


class TurnosHistorialView(LoginRequiredMixin, PacienteAccessMixin, TemplateView):
    template_name = "turnos/turnos_historial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_paciente()

        ahora = timezone.localtime()
        turnos = Turno.objects.filter(paciente=paciente)

        historial = []
        for t in turnos:
            dt = timezone.make_aware(datetime.combine(t.fecha, t.hora))
            t.es_vencido = False
            if t.estado.pk in (3, 5):
                historial.append(t)
            elif t.estado.pk == 2 and dt < ahora:
                t.es_vencido = True
                historial.append(t)

        historial_ordenado = sorted(historial, key=lambda t: (t.fecha, t.hora), reverse=True)
        context.update({
            "paciente": paciente,
            "turnos": historial_ordenado,
        })
        return context


class TurnosAgendadosView(LoginRequiredMixin, PacienteAccessMixin, TemplateView):
    template_name = "turnos/turnos_agendados.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paciente = self.get_paciente()

        ahora = timezone.localtime()

        turnos_confirmados = Turno.objects.filter(
            paciente=paciente,
            estado__pk=2
        )

        turnos_futuros = []
        for t in turnos_confirmados:
            dt = timezone.make_aware(datetime.combine(t.fecha, t.hora))

            if dt >= ahora:     # si ya pasó → va a historial
                turnos_futuros.append(t)

        turnos_ordenados = sorted(turnos_futuros, key=lambda t: (t.fecha, t.hora))

        context.update({
            "paciente": paciente,
            "turnos": turnos_ordenados,
        })
        return context


class VerTurnoView(LoginRequiredMixin, PacienteAccessMixin, TemplateView):
    template_name = "turnos/ver_turno.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        turno_id = kwargs.get("turno_id")

        paciente = self.get_paciente()

        turno = get_object_or_404(
            Turno.objects.select_related(
                "profesional",
                "profesional__especialidad",
                "paciente"
            ),
            id=turno_id,
            paciente=paciente
        )

        checkin_url = self.request.build_absolute_uri(
            reverse("turnos:checkin_qr") +
            f"?qr=TURNO:{turno.id};PACIENTE:{turno.paciente.id};FECHA:{turno.fecha};HORA:{turno.hora}"
        )

        context.update({
            "turno": turno,
            "paciente": paciente,
            "checkin_url": checkin_url,
            "desde_historial": "historial" in self.request.GET,
        })

        return context


class CancelarTurnoView(LoginRequiredMixin, PacienteAccessMixin, View):

    @transaction.atomic
    def post(self, request, paciente_id, turno_id):
        paciente = self.get_paciente()
        turno = get_object_or_404(Turno, pk=turno_id, paciente=paciente)

        ahora = timezone.localtime()
        dt_turno = timezone.make_aware(datetime.combine(turno.fecha, turno.hora))

        # 1) No se puede cancelar un turno asistido
        if turno.estado.pk == 3:
            messages.error(request, "Este turno ya fue asistido y no puede cancelarse.")
            return redirect("turnos:turnos_agendados", paciente_id=paciente_id)

        # 2) No se puede cancelar un turno ya cancelado
        if turno.estado.pk == 5:
            messages.error(request, "Este turno ya está cancelado.")
            return redirect("turnos:turnos_agendados", paciente_id=paciente_id)

        # 3) No se puede cancelar un turno vencido
        if dt_turno < ahora:
            messages.error(request, "No se puede cancelar un turno que ya pasó.")
            return redirect("turnos:turnos_agendados", paciente_id=paciente_id)

        estado_cancelado = Estado.objects.get(pk=5)
        estado_disponible = Estado.objects.get(pk=1)

        turno.estado = estado_cancelado
        turno.save()

        # Recrear turno plantilla
        Turno.objects.create(
            profesional=turno.profesional,
            fecha=turno.fecha,
            hora=turno.hora,
            modalidad=turno.modalidad,
            estado=estado_disponible,
            paciente=None
        )

        # Para profesionales híbridos, recrear modalidad espejo
        if turno.profesional.tipo_consulta == "AMBOS":
            modalidad_opuesta = "PRES" if turno.modalidad == "TELE" else "TELE"
            Turno.objects.create(
                profesional=turno.profesional,
                fecha=turno.fecha,
                hora=turno.hora,
                modalidad=modalidad_opuesta,
                estado=estado_disponible,
                paciente=None
            )

        messages.success(request, "El turno fue cancelado correctamente.")
        return redirect("turnos:turnos_agendados", paciente_id=paciente_id)

class CheckinQRView(View):

    def get(self, request, *args, **kwargs):
        qr_data = request.GET.get("qr")
        if not qr_data:
            return HttpResponse("QR inválido.")

        try:
            partes = qr_data.split(";")
            turno_id = partes[0].split(":")[1]
        except Exception:
            return HttpResponse("QR mal formado.")

        turno = get_object_or_404(Turno, pk=turno_id)
        ahora = timezone.localtime()

        # 1) Registrar check-in solo la primera vez
        primer_checkin = turno.check_in is None

        if primer_checkin:
            turno.check_in = ahora

            try:
                estado_asistido = Estado.objects.get(pk=3)
            except Estado.DoesNotExist:
                return HttpResponse("Estado 'Asistido' no encontrado.")

            if turno.estado.pk == 2:  # Confirmado
                turno.estado = estado_asistido

            turno.save()

            from .models import CheckInLog

            CheckInLog.objects.create(
                turno=turno,
                paciente=turno.paciente,
                llego_temprano=ahora < timezone.make_aware(
                    datetime.combine(turno.fecha, turno.hora)
                )
            )

        # 2) Calcular puntualidad
        horario_turno = timezone.make_aware(
            datetime.combine(turno.fecha, turno.hora)
        )
        llego_temprano = ahora < horario_turno

        # 3) Beneficio por puntualidad
        beneficio_otorgado = BeneficioOtorgado.objects.filter(
            turno=turno
        ).select_related("beneficio").first()

        beneficio_elegido = None

        if llego_temprano:
            if beneficio_otorgado:
                beneficio_elegido = beneficio_otorgado.beneficio
            else:
                beneficios_activos = list(Beneficio.objects.filter(activo=True))
                if beneficios_activos:
                    beneficio_elegido = random.choice(beneficios_activos)
                    BeneficioOtorgado.objects.create(
                        turno=turno,
                        paciente=turno.paciente,
                        beneficio=beneficio_elegido,
                        notificado=False
                    )

        return render(request, "turnos/checkin_confirmado.html", {
            "paciente": turno.paciente,
            "turno": turno,
            "ahora": ahora,
            "llego_temprano": llego_temprano,
            "beneficio_elegido": beneficio_elegido,
            "beneficio_otorgado": beneficio_otorgado,
        })