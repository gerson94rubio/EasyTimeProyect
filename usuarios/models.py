from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    # Opciones para el tipo de documento
    TIPO_DOC_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'NIT (Empresas)'),
        ('PP', 'Pasaporte'),
        ('TI', 'Tarjeta de Identidad'),
        ('PPT', 'Permiso por Proteccion Temporal'),
    ]
    
    tipo_documento = models.CharField(
        max_length=10,
        choices=TIPO_DOC_CHOICES, 
        default='CC'
    )

    # Esto cambia el texto "Username" por algo más profesional
    username = models.CharField(
        'Nombre de Usuario', # Etiqueta amigable
        max_length=150,
        unique=True,
        help_text='Nombre único para entrar al sistema.',
        error_messages={
            'unique': "Ya existe un usuario con este nombre.",
        },
    )

    identificacion = models.CharField(max_length=20, unique=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    # Roles para EasyTime
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('JEFE', 'Jefe de Patio'),
        ('CLIENTE', 'Cliente'),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='CLIENTE')

    def __str__(self):
        # Usamos self.username que viene de AbstractUser y nuestro campo rol
        return f"{self.username} - {self.get_rol_display()}"
    
    def save(self, *args, **kwargs):
        # Primero guardamos el usuario
        super().save(*args, **kwargs)
        
        # Si es Jefe de Patio, le damos acceso al admin automáticamente
        if self.rol == 'JEFE':
            self.is_staff = True
            # Aquí podrías agregar más lógica de grupos si quisieras
            super().save(update_fields=['is_staff'])