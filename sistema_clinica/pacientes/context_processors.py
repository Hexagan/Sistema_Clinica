def paciente_context(request):
    paciente = None
    paciente_id = None

    try:
        perfil = request.user.perfil
        if perfil and hasattr(perfil, "pacientes"):
            # último paciente usado en la sesión
            paciente_id = request.session.get("paciente_id")
            if paciente_id:
                paciente = perfil.pacientes.filter(id=paciente_id).first()
    except:
        pass

    return {
        "paciente": paciente,
        "paciente_id": paciente_id,
    }