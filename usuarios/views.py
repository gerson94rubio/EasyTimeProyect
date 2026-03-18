from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroClienteForm, EditarPerfilForm

def home(request):
    return render(request, 'home.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cuenta creada con éxito! Ya puedes iniciar sesión.")
            return redirect('login')
    else:
        form = RegistroClienteForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def mi_perfil(request):
    if request.method == 'POST':
            # instance=request.user le dice a Django que edite al usuario actual
         form = EditarPerfilForm(request.POST, instance=request.user)
         if form.is_valid():
            form.save()
            messages.success(request, "¡Tus datos han sido actualizados!")
            return redirect('mi_perfil')
    else:
            form = EditarPerfilForm(instance=request.user)
        
    return render(request, 'registration/perfil.html', {'form': form})