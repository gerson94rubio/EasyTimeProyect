from rest_framework import serializers
from .models import Producto

#aqui crearemos el serializer para el endpoint de Producto
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'