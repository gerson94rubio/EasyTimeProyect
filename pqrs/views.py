from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PQRS

@login_required
def mis_pqrs(request):
    # El cliente SOLO ve sus propias PQRS
    solicitudes = PQRS.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        asunto = request.POST.get('asunto')
        descripcion = request.POST.get('descripcion')
        
        PQRS.objects.create(
            usuario=request.user,
            tipo=tipo,
            asunto=asunto,
            descripcion=descripcion
        )
        messages.success(request, "Tu solicitud ha sido enviada correctamente.")
        return redirect('mis_pqrs')

    return render(request, 'mis_pqrs.html', {'solicitudes': solicitudes})