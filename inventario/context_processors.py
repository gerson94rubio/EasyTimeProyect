from .models import Venta, DetalleVenta
from django.db.models import Sum

def contador_carrito(request):
    total_items = 0
    # Solo buscamos si el usuario inició sesión
    if request.user.is_authenticated:
        # Buscamos la venta activa (carrito) del usuario
        carrito = Venta.objects.filter(cliente=request.user, pagado=False).first()
        
        if carrito:
            # Sumamos el campo 'cantidad' de todos los detalles de esa venta
            resultado = DetalleVenta.objects.filter(venta=carrito).aggregate(total=Sum('cantidad'))
            total_items = resultado['total'] or 0
            
    return {
        'contador_carrito': total_items
    }