from profesionales.models import Profesional

profesionales_nuevos = [
    # === 1 a 25 → un profesional extra por especialidad ===
    {
        "nombre": "Dr. Andrés Cabrera",
        "email": "acabrera@clinic.com",
        "matricula": "M-2001",
        "telefono": "11-5001-0001",
        "disponibilidad": "Lunes a Viernes",
        "consultorio": "401",
        "horario_inicio": "08:00",
        "horario_fin": "15:00",
        "dias_disponibles": "Lun-Mar-Mie-Jue-Vie",
        "especialidad_id": 1,
    },
    {
        "nombre": "Dra. Mariela Quiroga",
        "email": "mquiroga@clinic.com",
        "matricula": "M-2002",
        "telefono": "11-5001-0002",
        "disponibilidad": "Lunes a Sábado",
        "consultorio": "402",
        "horario_inicio": "09:00",
        "horario_fin": "16:00",
        "dias_disponibles": "Lun-Mar-Mie-Jue-Vie-Sab",
        "especialidad_id": 2,
    },
    {
        "nombre": "Dr. Emiliano Costa",
        "email": "ecosta@clinic.com",
        "matricula": "M-2003",
        "telefono": "11-5001-0003",
        "disponibilidad": "Martes a Sábado",
        "consultorio": "403",
        "horario_inicio": "10:00",
        "horario_fin": "18:00",
        "dias_disponibles": "Mar-Mie-Jue-Vie-Sab",
        "especialidad_id": 3,
    },
    {
        "nombre": "Dra. Teresa Beltrán",
        "email": "tbeltran@clinic.com",
        "matricula": "M-2004",
        "telefono": "11-5001-0004",
        "disponibilidad": "Lunes a Viernes",
        "consultorio": "404",
        "horario_inicio": "08:30",
        "horario_fin": "15:00",
        "dias_disponibles": "Lun-Mar-Mie-Jue-Vie",
        "especialidad_id": 4,
    },
    {
        "nombre": "Dr. Marcos Delgado",
        "email": "mdelgado@clinic.com",
        "matricula": "M-2005",
        "telefono": "11-5001-0005",
        "disponibilidad": "Lunes a Jueves",
        "consultorio": "405",
        "horario_inicio": "12:00",
        "horario_fin": "20:00",
        "dias_disponibles": "Lun-Mar-Mie-Jue",
        "especialidad_id": 5,
    },
]

# Generar automáticamente el resto (del 6 al 25)
mat = 2006
consult = 406
for esp in range(6, 26):
    profesionales_nuevos.append({
        "nombre": f"Dr./Dra. Profesional Extra {esp}",
        "email": f"pextra{esp}@clinic.com",
        "matricula": f"M-{mat}",
        "telefono": f"11-5001-{mat:04d}",
        "disponibilidad": "Lunes a Viernes",
        "consultorio": str(consult),
        "horario_inicio": "09:00",
        "horario_fin": "17:00",
        "dias_disponibles": "Lun-Mar-Mie-Jue-Vie",
        "especialidad_id": esp,
    })
    mat += 1
    consult += 1

# === Especialidades 26 a 30 → 2 profesionales cada una ===
for esp in range(26, 31):
    for k in range(2):
        profesionales_nuevos.append({
            "nombre": f"Dr./Dra. Profesional {esp}-{k+1}",
            "email": f"especialidad{esp}_{k+1}@clinic.com",
            "matricula": f"M-{mat}",
            "telefono": f"11-5001-{mat:04d}",
            "disponibilidad": "Martes a Sábado",
            "consultorio": str(consult),
            "horario_inicio": "10:00",
            "horario_fin": "18:00",
            "dias_disponibles": "Mar-Mie-Jue-Vie-Sab",
            "especialidad_id": esp,
        })
        mat += 1
        consult += 1

# === Guardar ===
for p in profesionales_nuevos:
    Profesional.objects.get_or_create(**p)

print("✔ Se crearon 35 profesionales nuevos (2 por especialidad).")
