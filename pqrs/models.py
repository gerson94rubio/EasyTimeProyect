from django.db import models
from django.conf import settings

class PQRS(models.Model):
    TIPOS = [
        ('PETICION', 'Petición'),
        ('QUEJA', 'Queja'),
        ('RECLAMO', 'Reclamo'),
        ('SUGERENCIA', 'Sugerencia'),
    ]
    
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_REVISION', 'En Revisión'),
        ('RESUELTA', 'Resuelta'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='PETICION')
    asunto = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    respuesta_admin = models.TextField(blank=True, null=True, help_text="Respuesta oficial del autolavado")

    class Meta:
        verbose_name = "PQRS"
        verbose_name_plural = "PQRS"

    def __str__(self):
        return f"{self.tipo} - {self.asunto} ({self.usuario.username})"

# Create your models here.
