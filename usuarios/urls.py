from django.urls import path
from . import views

urlpatterns = [
    # URLs para gestión de usuarios (solo admin)
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # URLs para perfil de usuario (cada usuario puede ver/editar su propio perfil)
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),
    path('editar-perfil/', views.editar_mi_perfil, name='editar_mi_perfil'),
]