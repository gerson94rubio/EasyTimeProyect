from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cita
from .forms import CitaForm  # <--- Importamos el formulario
from django.contrib import messages
from django.db import IntegrityError

@login_required
def agendar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST) # Cargamos los datos del POST al formulario
        if form.is_valid():
            try:
                cita = form.save(commit=False)
                cita.usuario = request.user
                cita.save()
                messages.success(request, "¡Cita agendada con éxito!")
                return redirect('mis_citas')
            except IntegrityError: # Captura específicamente el error de hora duplicada
                messages.error(request, "Error: Esa fecha y hora ya están ocupadas.")
    else:
        form = CitaForm() # Formulario vacío para GET
            
    return render(request, 'agendar.html', {'form': form})

@login_required
def mis_citas(request):
    citas = Cita.objects.filter(usuario=request.user).order_by('-fecha_hora')
    return render(request, 'mis_citas.html', {'citas': citas})