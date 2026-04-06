from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.models import User 
from agendamiento.models import Cita
from django.utils import timezone

"""@user_passes_test(lambda u: u.is_staff) Por ahora no haremos Dashboard
def dashboard_admin(request):
    context = {
        'total_usuarios': User.objects.count(),
        'total_citas': Cita.objects.count(),
        'citas_hoy': Cita.objects.filter(fecha_hora__date=timezone.now().date()).count(),
        'proximas_citas': Cita.objects.filter(fecha_hora__gte=timezone.now()).order_by('fecha_hora')[:5],
        'ultimos_usuarios': User.objects.all().order_by('-date_joined')[:5],
    }
    return render(request, 'dashboard.html', context)
"""

def home(request):
    return render(request, 'home.html')

@login_required
def gestion_citas(request):
    from usuarios.views import es_admin
    if not es_admin(request.user):
        return redirect('home')
    citas = Cita.objects.all().order_by('-fecha_hora')
    return render(request, 'gestion_citas.html', {'citas': citas})
