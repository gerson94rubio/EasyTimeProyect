from django.db import models
from django.conf import settings # Para referenciar a tu modelo de Usuario personalizado

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.DurationField(help_text="Formato: HH:MM:SS")
    # CORRECCIÓN: Añadimos el campo de imagen para que se vea en el catálogo
    imagen = models.ImageField(upload_to='servicios/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Cita(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    # Relación con el Usuario (quién pide la cita)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT,
        related_name='citas'
    )
    # Relación con el Servicio (qué se va a hacer)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    
    fecha_hora = models.DateTimeField()
    placa_vehiculo = models.CharField(max_length=10) # Podría ser FK a un modelo Vehiculo luego
    notas = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    creado_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agendamiento"
        verbose_name_plural = "Agendamientos"
        # Evita que agenden dos citas a la misma hora exacta (básico para el Ítem 8)
        unique_together = ['fecha_hora']

    def __str__(self):
        return f"Cita {self.id}: {self.usuario.username} - {self.fecha_hora}"


class Notificacion(models.Model):  # ← ✅ BIEN: Al mismo nivel que Cita
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return self.mensaje