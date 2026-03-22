from django.contrib import admin
from .models import Servicio, Cita
from django.urls import path
from django.shortcuts import render

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    # Columnas que se ven en la tabla principal
    list_display = ('nombre', 'precio', 'duracion_estimada')
    search_fields = ('nombre',)
    
    # Esto asegura que al entrar a editar un servicio, veas los campos nuevos
    # Si quieres organizar el orden, puedes usar 'fields'
    fields = ('nombre', 'descripcion', 'precio', 'duracion_estimada', 'imagen')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'servicio', 'fecha_hora', 'estado', 'placa_vehiculo')
    list_filter = ('estado', 'fecha_hora', 'servicio')
    # Nota: Asegúrate de que el modelo Usuario tenga el campo 'identificacion' para que search_fields no de error
    search_fields = ('usuario__username', 'placa_vehiculo') 
    date_hierarchy = 'fecha_hora'
    list_per_page = 15

    # Lógica para el botón de reporte
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('reporte-agendas/', self.admin_site.admin_view(self.reporte_agendamiento_view)),
        ]
        return custom_urls + urls

    def reporte_agendamiento_view(self, request):
        agendas = self.model.objects.all()
        # El template debe existir en tu carpeta de templates
        return render(request, 'reporte_agendamiento.html', {'agendas': agendas})

# El registro ya se hizo con los decoradores @admin.register