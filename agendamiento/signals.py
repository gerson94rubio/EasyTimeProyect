from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Q  

@receiver(post_save, sender='agendamiento.Cita')
def notificar_nueva_cita(sender, instance, created, **kwargs):
    if created:
        from .models import Notificacion
        User = get_user_model()
        
        # ← CAMBIA ESTO:
        administradores = User.objects.filter(
            Q(is_staff=True) | Q(rol='ADMIN') | Q(rol='JEFE')
        )
        
        for admin in administradores:
            Notificacion.objects.create(
                usuario=admin,
                mensaje=f"🚗 Nueva cita: {instance.usuario.username} - {instance.fecha_hora}"
            )