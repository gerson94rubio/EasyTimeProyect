from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User # Asegúrate de importar tu modelo personalizado

class RegistroClienteForm(UserCreationForm):
    # Añadimos los campos explícitamente para que sean obligatorios
    first_name = forms.CharField(label="Nombres", required=True)
    last_name = forms.CharField(label="Apellidos", required=True)
    email = forms.EmailField(label="Correo Electrónico", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'email', 'tipo_documento', 'identificacion', 'telefono'
        )

# NUEVO: Formulario para editar el perfil
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['telefono', 'first_name', 'last_name'] # Solo lo que puede cambiar
        # El correo y la identificación NO se incluyen aquí para que no los edite

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'CLIENTE' # Forzamos que siempre sea CLIENTE por seguridad
        if commit:
            user.save()
        return user
    

# ===================================================================
# NUEVOS: Formularios para administración (Admin/Jefe)
# ===================================================================

class UsuarioCreationForm(UserCreationForm):
    """Formulario para crear usuarios (solo admin)"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 
                    'identificacion', 'tipo_documento', 'telefono', 'rol']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

class UsuarioUpdateForm(forms.ModelForm):
    """Formulario para actualizar usuarios (solo admin)"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 
                    'identificacion', 'tipo_documento', 'telefono', 'rol']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que los campos no sean requeridos si ya tienen valor
        for field in self.fields.values():
            field.required = False