from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Proveedor, Producto, EntradaInventario, DetalleEntrada, Venta, DetalleVenta

# --- INLINES (Para ver los "Carritos" dentro de cada registro) ---

class DetalleEntradaInline(admin.TabularInline):
    model = DetalleEntrada
    extra = 1

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0 # No permitimos agregar manualmente para no alterar el carrito
    readonly_fields = ('producto', 'cantidad', 'precio_unitario')

# --- CONFIGURACIÓN DE VISTAS ---

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'stock_actual', 'precio_venta')
    search_fields = ('nombre',)

    # Botón para Reporte de Inventario
    def get_urls(self):
        urls = super().get_urls()
        return [path('reporte-stock/', self.admin_site.admin_view(self.reporte_stock_view))] + urls

    def reporte_stock_view(self, request):
        productos = Producto.objects.all()
        return render(request, 'reporte_inventario.html', {'productos': productos})

@admin.register(EntradaInventario)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha_registro')
    inlines = [DetalleEntradaInline]

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_venta', 'total', 'pagado')
    list_filter = ('pagado', 'fecha_venta')
    inlines = [DetalleVentaInline]

    # Botón para Reporte de Ventas (El dinero que entró por el carrito)
    def get_urls(self):
        urls = super().get_urls()
        return [path('reporte-ventas/', self.admin_site.admin_view(self.reporte_ventas_view))] + urls

    def reporte_ventas_view(self, request):
        ventas = Venta.objects.all()
        total_ganado = sum(v.total for v in ventas)
        return render(request, 'reporte_ventas.html', {'ventas': ventas, 'total_ganado': total_ganado})

admin.site.register(Proveedor)