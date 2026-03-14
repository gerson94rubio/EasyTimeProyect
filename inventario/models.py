from django.db import models
from django.conf import settings

# --- 1. SECCIÓN DE ABASTECIMIENTO (ADMIN) ---

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio para el cliente")
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio_venta})"

class EntradaInventario(models.Model):
    """Registro de cuando el proveedor trae mercancía"""
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Entrada #{self.id} - {self.proveedor}"

class DetalleEntrada(models.Model):
    """Items específicos que entraron al almacén"""
    entrada = models.ForeignKey(EntradaInventario, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_recibida = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Al recibir mercancía, el stock aumenta
        self.producto.stock_actual += self.cantidad_recibida
        self.producto.save()
        super().save(*args, **kwargs)

# --- 2. SECCIÓN DE VENTAS (CARRITO DEL CLIENTE) ---

class Venta(models.Model):
    """La orden final generada por el cliente"""
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.username}"

class DetalleVenta(models.Model):
    """Los productos que el cliente 'echo al carrito'"""
    venta = models.ForeignKey(Venta, related_name='items_venta', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Precio al momento de la venta

    def save(self, *args, **kwargs):
        # Al vender, el stock disminuye
        if self.producto.stock_actual >= self.cantidad:
            self.producto.stock_actual -= self.cantidad
            self.producto.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError("No hay suficiente stock para esta venta")
