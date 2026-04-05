from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.paginator import Paginator # Importante para el catálogo
from .models import Cita, Servicio, Notificacion 
from .forms import CitaForm

# ===================================================================
# CATÁLOGO Y AGENDAMIENTO
# ===================================================================

def lista_servicios(request):
    """Muestra el catálogo con paginación de 6 servicios (Ruta corregida)"""
    servicios_list = Servicio.objects.all().order_by('nombre')
    paginator = Paginator(servicios_list, 6) #
    
    page_number = request.GET.get('page')
    servicios = paginator.get_page(page_number)
    
    # El template está en la raíz de templates/ según tu estructura
    return render(request, 'servicios.html', {'servicios': servicios})

@login_required
def agendar_cita(request, servicio_id=None):
    """Permite agendar una cita, opcionalmente con un servicio preseleccionado"""
    servicio_seleccionado = None
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
        initial_data = {'servicio': servicio_seleccionado} if servicio_seleccionado else {}
        form = CitaForm(initial=initial_data) 
            
    return render(request, 'agendar.html', {
        'form': form, 
        'servicio_seleccionado': servicio_seleccionado
    })

@login_required
def mis_citas(request):
    """Historial de citas del usuario actual"""
    citas = Cita.objects.filter(usuario=request.user).order_by('-fecha_hora')
    return render(request, 'mis_citas.html', {'citas': citas})

# ===================================================================
# SISTEMA DE NOTIFICACIONES
# ===================================================================

@login_required
def obtener_notificaciones(request):
    """Endpoint para el navbar (Actualización en tiempo real)"""
    es_admin_jefe = getattr(request.user, 'rol', None) in ['ADMIN', 'JEFE'] #
    
    if request.user.is_staff or es_admin_jefe:
        notificaciones = Notificacion.objects.filter(
            usuario=request.user, 
            leida=False
        ).order_by('-fecha')[:10]
        
        datos = [{
            'id': noti.id,
            'mensaje': noti.mensaje,
            'fecha': noti.fecha.strftime('%H:%M'),
        } for noti in notificaciones]
        
        return JsonResponse({'notificaciones': datos, 'count': len(datos)})
    
    return JsonResponse({'notificaciones': [], 'count': 0})

@login_required
def marcar_leida(request, notificacion_id):
    """Marca como leída una notificación específica"""
    if request.method == 'POST':
        notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
        notificacion.leida = True
        notificacion.save()
        return JsonResponse({'status': 'ok'}) # Corregida indentación
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def ver_notificacion_detalle(request, notificacion_id):
    """Muestra detalles y marca como leída al abrir"""
    es_admin_jefe = getattr(request.user, 'rol', None) in ['ADMIN', 'JEFE']
    
    if not (request.user.is_staff or es_admin_jefe):
        messages.error(request, "No tienes permisos para ver esta notificación")
        return redirect('home')
    
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    
    # Obtenemos la última cita relacionada para mostrar contexto
    cita = Cita.objects.order_by('-creado_el').first() 
    
    return render(request, 'notificacion_detalle.html', {
        'notificacion': notificacion,
        'cita': cita,
    })

@login_required
def ver_todas_las_notificaciones(request):
    """Historial completo de alertas"""
    es_admin_jefe = getattr(request.user, 'rol', None) in ['ADMIN', 'JEFE']
    
    if not (request.user.is_staff or es_admin_jefe):
        messages.error(request, "Acceso denegado")
        return redirect('home')
    
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')[:50]
    return render(request, 'todas_las_notificaciones.html', {'notificaciones': notificaciones})