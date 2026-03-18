from django.contrib import admin
from .models import PQRS

@admin.register(PQRS)
class PQRSAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'tipo', 'asunto', 'fecha_creacion', 'estado')
    list_filter = ('estado', 'tipo', 'fecha_creacion')
    search_fields = ('asunto', 'usuario__username')
    
    # El admin solo escribe la respuesta y cambia el estado
    fields = ('usuario', 'tipo', 'asunto', 'descripcion', 'estado', 'respuesta_admin')
    readonly_fields = ('usuario', 'tipo', 'asunto', 'descripcion', 'fecha_creacion')

    # Color para los estados en la lista
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-fecha_creacion')

# Register your models here.
