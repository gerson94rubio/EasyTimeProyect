from django.urls import path
from . import views

urlpatterns = [
    # ===================================================================
    # DASHBOARD Y VISTAS PRINCIPALES
    # ===================================================================
    # Ruta del nuevo Dashboard exclusivo para ADMIN
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Perfil del usuario autenticado
    path('perfil/', views.mi_perfil, name='mi_perfil'),
    
    # Registro de nuevos clientes
    path('registro/', views.registro_cliente, name='registro'),

    # ===================================================================
    # GESTIÓN DE USUARIOS (CRUD) - Solo personal autorizado
    # ===================================================================
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),

    # ===================================================================
    # EXPORTACIÓN DE REPORTES
    # ===================================================================
    # Estas rutas reciben parámetros (?scope=pagina o ?scope=todo) en el navegador
    path('reporte-pdf/', views.generar_pdf_usuarios, name='generar_pdf_usuarios'),
    path('reporte-excel/', views.generar_excel_usuarios, name='generar_excel_usuarios'),
]