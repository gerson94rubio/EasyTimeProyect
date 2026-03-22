from django.contrib.auth.models import AbstractUser
from django.db import models

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

    # Nombre de usuario con etiqueta amigable
    username = models.CharField(
        'Nombre de Usuario',
        max_length=150,
        unique=True,
        help_text='Nombre único para entrar al sistema.',
        error_messages={
            'unique': "Ya existe un usuario con este nombre.",
        },
    )

    identificacion = models.CharField(max_length=20, unique=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    # Roles definidos para el sistema EasyTime
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('JEFE', 'Jefe de Patio'),
        ('CLIENTE', 'Cliente'),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='CLIENTE')

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
    
    def save(self, *args, **kwargs):
        # LOGICA DE SEGURIDAD:
        # Solo permitimos 'is_staff' (acceso al panel admin) si el rol es ADMIN o JEFE.
        # También verificamos si ya es superusuario para no quitarle el permiso por accidente.
        if self.rol in ['ADMIN', 'JEFE'] or self.is_superuser:
            self.is_staff = True
        else:
            # Los CLIENTES siempre tendrán is_staff en False, bloqueando su acceso al admin.
            self.is_staff = False
        
        # Guardamos los cambios en la base de datos
        super().save(*args, **kwargs)