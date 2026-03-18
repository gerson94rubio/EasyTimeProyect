from django import forms
from .models import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        # Estos son los campos que el CLIENTE debe llenar
        fields = ['servicio', 'fecha_hora', 'placa_vehiculo', 'notas']
        
        # Aquí le damos el diseño de Bootstrap y los tipos de entrada correctos
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'placa_vehiculo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: ABC-123'}
            ),
            'notas': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalles adicionales...'}
            ),
        }
        labels = {
            'fecha_hora': 'Fecha y Hora de la Cita',
            'placa_vehiculo': 'Placa del Vehículo',
            'servicio': 'Tipo de Servicio',
        }