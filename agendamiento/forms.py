from django import forms
from .models import Cita, Servicio
from django.utils import timezone
from django.core.exceptions import ValidationError

class CitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        # 1. CORRECCIÓN: En el selector solo se verá el nombre (ej: "Lavado Rápido")
        # El precio se quita de aquí porque ya lo mostramos en el cuadro azul.
        self.fields['servicio'].label_from_instance = lambda obj: f"{obj.nombre}"

    class Meta:
        model = Cita
        fields = ['servicio', 'fecha_hora', 'placa_vehiculo', 'notas']
        
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local', 
                    'class': 'form-control',
                    # 2. SUGERENCIA: Bloqueo visual en el calendario (HTML5)
                    'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'placa_vehiculo': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ej: ABC-123',
                    'style': 'text-transform: uppercase;' # Se ve en mayúsculas mientras escribe
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

    # 3. VALIDACIÓN DE FECHA (Lógica de Servidor)
    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data.get('fecha_hora')
        # Si la fecha es menor a "ahora", lanzamos el error
        if fecha_hora and fecha_hora < timezone.now():
            raise ValidationError("No puedes agendar una cita en una fecha o hora que ya pasó.")
        return fecha_hora

    # 4. LIMPIEZA DE PLACA (Asegura mayúsculas en BD)
    def clean_placa_vehiculo(self):
        placa = self.cleaned_data.get('placa_vehiculo')
        return placa.upper() if placa else placa