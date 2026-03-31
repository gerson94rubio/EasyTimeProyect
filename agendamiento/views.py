from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cita, Servicio, Notificacion 
from .models import Cita, Servicio 
from .forms import CitaForm
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse

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

@login_required
def obtener_notificaciones(request):
    if request.user.is_staff:
        notificaciones = Notificacion.objects.filter(
            usuario=request.user, 
            leida=False
        )[:10]
        
        datos = [{
            'id': noti.id,
            'mensaje': noti.mensaje,
            'fecha': noti.fecha.strftime('%H:%M'),
        } for noti in notificaciones]
        
        return JsonResponse({'notificaciones': datos, 'count': len(datos)})
    
    return JsonResponse({'notificaciones': [], 'count': 0})

@login_required
def marcar_leida(request, notificacion_id):
    if request.method == 'POST' and request.user.is_staff:
                notificacion = Notificacion.objects.get(
            id=notificacion_id, 
            usuario=request.user
        )
    notificacion.leida = True
    notificacion.save()
    return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def ver_notificacion_detalle(request, notificacion_id):
    """Muestra los detalles de una notificación y la cita asociada"""
    if not (request.user.is_staff or request.user.rol in ['ADMIN', 'JEFE']):
        messages.error(request, "No tienes permisos para ver esta notificación")
        return redirect('home')
    
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    
    # Marcar como leída
    notificacion.leida = True
    notificacion.save()
    
    # Buscar la cita más reciente
    cita = Cita.objects.order_by('-creado_el').first()
    
    context = {
        'notificacion': notificacion,
        'cita': cita,
    }
    return render(request, 'notificacion_detalle.html', context)


@login_required
def ver_todas_las_notificaciones(request):
    """Muestra todas las notificaciones del usuario"""
    if not (request.user.is_staff or request.user.rol in ['ADMIN', 'JEFE']):
        messages.error(request, "No tienes permisos")
        return redirect('home')
    
    notificaciones = Notificacion.objects.filter(
        usuario=request.user
    ).order_by('-fecha')[:50]
    
    return render(request, 'todas_las_notificaciones.html', {'notificaciones': notificaciones})