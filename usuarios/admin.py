from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render
from django.urls import path
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id','first_name','last_name','identificacion','tipo_documento','telefono','username', 'email', 'rol', 'is_active', 'is_staff')
    # Añadido para poder tener "enlaces" en cada campo para editar usuario
    list_display_links = ('id','first_name','last_name','identificacion','tipo_documento','telefono','username', 'email', 'rol', 'is_active', 'is_staff') 
    search_fields = ('id','first_name','last_name','identificacion','tipo_documento','telefono','username', 'email', 'rol',)
    list_filter = ('rol', 'tipo_documento', 'is_active')

    list_per_page = 10
    
    # Nota: He unido los fieldsets para que no se repitan
    fieldsets = UserAdmin.fieldsets + (
        ('Información de EasyTime', {
            'fields': ('tipo_documento', 'identificacion', 'telefono', 'rol')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de EasyTime', {
            'fields': ('tipo_documento', 'identificacion', 'telefono', 'rol')
        }),
    )

    actions = ['exportar_a_pdf']

    @admin.action(description="Generar Reporte de Usuarios (PDF)")
    def exportar_a_pdf(self, request, queryset):
        # Todo esto DEBE tener 2 tabulaciones (8 espacios) desde el borde
        usuarios = queryset 
        
        if not usuarios:
            usuarios = self.model.objects.all()

        return render(request, 'reporte_usuarios.html', {'usuarios': usuarios})
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # Esta URL debe coincidir con el href del HTML anterior
            path('print-report/', self.admin_site.admin_view(self.reporte_general_view)),
        ]
        return custom_urls + urls

    def reporte_general_view(self, request):
        # Aquí tomamos a TODOS los usuarios de la base de datos
        usuarios = self.model.objects.all()
        return render(request, 'reporte_usuarios.html', {'usuarios': usuarios})