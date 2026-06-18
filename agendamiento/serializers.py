from rest_framework import serializers
from .models import Cita, Servicio

class CitaSerializer(serializers.ModelSerializer):
    servicio = serializers.SlugRelatedField(
        queryset=Servicio.objects.all(),
        slug_field='nombre'
    )
    class Meta:
        model = Cita
        fields = '__all__'