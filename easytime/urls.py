"""
URL configuration for easytime project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from agendamiento import views as agend_views
from inventario import views as inv_views
from pqrs import views as pqrs_views
from usuarios import views as usuarios_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', usuarios_views.custom_logout, name='logout'), 

    # --- AGENDAMIENTO ---
    path('agendar/', agend_views.agendar_cita, name='agendar'),
    path('mis-citas/', agend_views.mis_citas, name='mis_citas'),

    # --- INVENTARIO / CARRITO ---
    path('productos/', inv_views.catalogo_productos, name='catalogo_productos'),
    path('carrito/', inv_views.ver_carrito, name='ver_carrito'),
    path('comprar/<int:producto_id>/', inv_views.agregar_al_carrito, name='agregar_carrito'),
    path('pagar/<int:venta_id>/', inv_views.finalizar_compra, name='finalizar_compra'),
    # Eliminamos la línea duplicada y corregimos el prefijo a inv_views:
    path('eliminar-del-carrito/<int:item_id>/', inv_views.eliminar_del_carrito, name='eliminar_item'),

    # --- PQRS ---
    path('pqrs/', pqrs_views.mis_pqrs, name='mis_pqrs'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)