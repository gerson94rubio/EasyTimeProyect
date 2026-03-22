from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Venta, DetalleVenta
from django.db import transaction

# Catálogo de EasyTime
def catalogo_productos(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})

# Agregar al carrito
@login_required
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    try:
        cantidad_a_añadir = int(request.POST.get('cantidad', 1)) if request.method == 'POST' else 1
    except ValueError:
        cantidad_a_añadir = 1
    
    venta, created = Venta.objects.get_or_create(cliente=request.user, pagado=False)
    detalle = DetalleVenta.objects.filter(venta=venta, producto=producto).first()
    
    if detalle:
        detalle.cantidad += cantidad_a_añadir
        detalle.save()
        messages.info(request, f"Se actualizó la cantidad de {producto.nombre}.")
    else:
        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            # Se asume que el modelo DetalleVenta tiene el campo 'cantidad'
            cantidad=cantidad_a_añadir,
            precio_unitario=producto.precio_venta
        )
        messages.success(request, f"{producto.nombre} añadido al carrito.")
    
    return redirect('catalogo_productos')

@login_required
def ver_carrito(request):
    carrito = Venta.objects.filter(cliente=request.user, pagado=False).first()
    return render(request, 'carrito.html', {'carrito': carrito})

# --- NUEVA VISTA: PASARELA DE PAGO SIMULADA ---
@login_required
def pasarela_pago(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id, cliente=request.user, pagado=False)
    
    # Si viene del carrito, capturamos qué items seleccionó para pagar
    items_ids = request.POST.getlist('items_seleccionados')
    
    if not items_ids and request.method == 'POST':
        messages.error(request, "Selecciona al menos un producto para pagar.")
        return redirect('ver_carrito')

    # Obtenemos los detalles específicos para mostrar el resumen en la pasarela
    detalles_a_pagar = venta.items_venta.filter(id__in=items_ids)
    total = sum(item.producto.precio_venta * item.cantidad for item in detalles_a_pagar)

    return render(request, 'pasarela.html', {
        'venta': venta,
        'items_ids': items_ids, # Pasamos los IDs para que el formulario final los procese
        'detalles': detalles_a_pagar,
        'total': total
    })

@login_required
def finalizar_compra(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id, cliente=request.user)
    
    if request.method == 'POST':
        # Capturamos los IDs que vienen desde el formulario oculto de la pasarela
        items_ids = request.POST.getlist('items_seleccionados')
        
        if not items_ids:
            messages.error(request, "No hay productos seleccionados para procesar.")
            return redirect('ver_carrito')

        with transaction.atomic():
            detalles_a_pagar = venta.items_venta.filter(id__in=items_ids)
            detalles_a_conservar = venta.items_venta.exclude(id__in=items_ids)

            # Validación de Stock
            for item in detalles_a_pagar:
                if item.producto.stock_actual < item.cantidad:
                    messages.error(request, f"Stock insuficiente para {item.producto.nombre}")
                    return redirect('ver_carrito')

            # Si sobran productos, creamos un nuevo carrito para el futuro
            if detalles_a_conservar.exists():
                nuevo_carrito = Venta.objects.create(cliente=request.user, pagado=False)
                detalles_a_conservar.update(venta=nuevo_carrito)

            # Descontar stock
            for item in detalles_a_pagar:
                item.producto.stock_actual -= item.cantidad
                item.producto.save()
            
            # Marcar como pagada
            venta.pagado = True
            venta.save()
        
        messages.success(request, "¡Pago simulado con éxito! Pedido confirmado.")
        return redirect('catalogo_productos')
    
    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(DetalleVenta, id=item_id, venta__cliente=request.user)
    item.delete()
    messages.warning(request, "Producto eliminado.")
    return redirect('ver_carrito')