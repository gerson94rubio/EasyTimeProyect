from django.urls import path
from . import views

app_name = 'agendamiento'

urlpatterns = [
    path('api/notificaciones/', views.obtener_notificaciones, name='obtener_notificaciones'),
    path('notificacion/<int:notificacion_id>/marcar-leida/', views.marcar_leida, name='marcar_leida'),
    path('notificacion/<int:notificacion_id>/detalle/', views.ver_notificacion_detalle, name='ver_notificacion_detalle'),
    path('notificaciones/', views.ver_todas_las_notificaciones, name='ver_todas_las_notificaciones'),
]
