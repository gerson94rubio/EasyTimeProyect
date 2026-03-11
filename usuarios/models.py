from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, null=True)
    identificacion = models.CharField(max_length=20, unique=True, null=True)
    
    # Roles para EasyTime
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('JEFE', 'Jefe de Patio'),
        ('CLIENTE', 'Cliente'),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='CLIENTE')

    def __str__(self):
        return f"{self.username} - {self.rol}"