from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Venta, DetalleVenta

def catalogo_productos(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Buscamos una venta que no esté pagada (el carrito actual del usuario)
    # Si no existe, la creamos
    venta, created = Venta.objects.get_or_create(
        cliente=request.user, 
        pagado=False
    )
    
    # Añadimos el producto al detalle
    DetalleVenta.objects.create(
        venta=venta,
        producto=producto,
        cantidad=1,
        precio_unitario=producto.precio_venta
    )
    
    messages.success(request, f"{producto.nombre} se añadió al carrito.")
    return redirect('catalogo_productos')

@login_required
def ver_carrito(request):
    # Buscamos el carrito activo del usuario
    carrito = Venta.objects.filter(cliente=request.user, pagado=False).first()
    return render(request, 'carrito.html', {'carrito': carrito})

@login_required
def finalizar_compra(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id, cliente=request.user)
    
    # AQUÍ ES DONDE SE BAJA EL STOCK
    for item in venta.items_venta.all():
        if item.producto.stock_actual >= item.cantidad:
            item.producto.stock_actual -= item.cantidad
            item.producto.save()
        else:
            messages.error(request, f"No hay stock suficiente de {item.producto.nombre}")
            return redirect('ver_carrito')
    
    venta.pagado = True
    venta.save()
    messages.success(request, "¡Compra realizada con éxito! El inventario ha sido actualizado.")
    return redirect('catalogo_productos')

# ... (tus otros imports y la función catalogo_productos y agregar_al_carrito) ...

def ver_carrito(request):
    # Buscamos la venta activa (carrito) del usuario actual
    carrito = Venta.objects.filter(cliente=request.user, pagado=False).first()
    return render(request, 'carrito.html', {'carrito': carrito})

@login_required
def finalizar_compra(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id, cliente=request.user)
    
    # Verificamos stock de cada producto antes de confirmar
    detalles = venta.items_venta.all() # Usamos el related_name que definimos en el modelo
    
    for item in detalles:
        if item.producto.stock_actual < item.cantidad:
            messages.error(request, f"No hay suficiente stock de {item.producto.nombre}")
            return redirect('ver_carrito')

    # Si todo está OK, descontamos el stock y marcamos como pagado
    for item in detalles:
        item.producto.stock_actual -= item.cantidad
        item.producto.save()
    
    venta.pagado = True
    venta.save()
    
    messages.success(request, "¡Compra finalizada con éxito! El inventario se ha actualizado.")
    return redirect('catalogo_productos')

@login_required
def eliminar_del_carrito(request, item_id):
    # Esta es la función que te faltaba y causaba el AttributeError
    item = get_object_or_404(DetalleVenta, id=item_id, venta__cliente=request.user)
    item.delete()
    messages.warning(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')