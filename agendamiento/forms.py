from django import forms
from .models import Cita, Servicio
from django.utils import timezone
from django.core.exceptions import ValidationError

class CitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        
        # ✅ AGREGA ESTA LÍNEA:
        self.fields['servicio'].queryset = Servicio.objects.all()
        
        self.fields['servicio'].label_from_instance = lambda obj: f"{obj.nombre}"

    class Meta:
        model = Cita
        fields = ['servicio', 'fecha_hora', 'placa_vehiculo', 'notas']
        
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 
                    'class': 'form-control',
                    'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'placa_vehiculo': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ej: ABC-123',
                    'style': 'text-transform: uppercase;'
                }
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

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if fecha_hora and fecha_hora < timezone.now():
            raise ValidationError("No puedes agendar una cita en una fecha o hora que ya pasó.")
        return fecha_hora

    def clean_placa_vehiculo(self):
        placa = self.cleaned_data.get('placa_vehiculo')
        return placa.upper() if placa else placa