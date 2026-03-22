from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cita, Servicio 
from .forms import CitaForm
from django.contrib import messages
from django.db import IntegrityError

def lista_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios.html', {'servicios': servicios})

@login_required
def agendar_cita(request, servicio_id=None): # Añadimos el parámetro opcional
    servicio_seleccionado = None
    
    # Si viene un ID en la URL, buscamos el servicio
    if servicio_id:
        servicio_seleccionado = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        form = CitaForm(request.POST) 
        if form.is_valid():
            try:
                cita = form.save(commit=False)
                cita.usuario = request.user
                cita.save()
                messages.success(request, "¡Cita agendada con éxito!")
                return redirect('mis_citas')
            except IntegrityError: 
                messages.error(request, "Error: Esa fecha y hora ya están ocupadas.")
    else:
        # CORRECCIÓN: Si hay un servicio seleccionado, lo pasamos como valor inicial al formulario
        initial_data = {}
        if servicio_seleccionado:
            initial_data['servicio'] = servicio_seleccionado
        
        form = CitaForm(initial=initial_data) 
            
    return render(request, 'agendar.html', {'form': form, 'servicio_seleccionado': servicio_seleccionado})

@login_required
def mis_citas(request):
    citas = Cita.objects.filter(usuario=request.user).order_by('-fecha_hora')
    return render(request, 'mis_citas.html', {'citas': citas})