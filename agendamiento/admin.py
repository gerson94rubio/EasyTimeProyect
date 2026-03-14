from django.contrib import admin
from .models import Servicio, Cita
from django.urls import path
from django.shortcuts import render

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_estimada')
    search_fields = ('nombre',)

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'servicio', 'fecha_hora', 'estado', 'placa_vehiculo')
    list_filter = ('estado', 'fecha_hora', 'servicio')
    search_fields = ('usuario__username', 'placa_vehiculo', 'usuario__identificacion')
    date_hierarchy = 'fecha_hora' # Esto añade un navegador de fechas arriba (muy pro)
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
        # Usaremos el mismo master, pero un template nuevo para este módulo
        return render(request, 'reporte_agendamiento.html', {'agendas': agendas})

# Register your models here.
