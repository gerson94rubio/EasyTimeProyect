from django.db import models
from django.conf import settings

class PQRS(models.Model):
    TIPO_CHOICES = [
        ('Peticion', 'Petición'),
        ('Queja', 'Queja'),
        ('Reclamo', 'Reclamo'),
        ('Sugerencia', 'Sugerencia'),
    ]
    
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Resuelto', 'Resuelto'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    
    # Este es el campo que le faltaba a tu lógica anterior
    respuesta_admin = models.TextField(blank=True, null=True, verbose_name="Respuesta del Administrador")

    def __str__(self):
        return f"{self.tipo} - {self.asunto} ({self.usuario.username})"

    class Meta:
        verbose_name_plural = "PQRS"