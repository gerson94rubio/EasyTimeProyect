from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .forms import RegistroClienteForm, EditarPerfilForm, UsuarioCreationForm, UsuarioUpdateForm
from .models import User

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

# ===================================================================
# ADMINISTRACIÓN DE USUARIOS (Solo para ADMIN y JEFE)
# ===================================================================

def es_admin(user):
    """Verifica si el usuario es ADMIN, JEFE o superuser"""
    return user.is_authenticated and (user.rol in ['ADMIN', 'JEFE'] or user.is_superuser)

@login_required
@user_passes_test(es_admin, login_url='home')
def lista_usuarios(request):
    """Muestra la lista de todos los usuarios"""
    usuarios = User.objects.all().order_by('first_name')
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_admin, login_url='home')
def crear_usuario(request):
    """Crea un nuevo usuario"""
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('lista_usuarios')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/form_usuario.html', {'form': form, 'titulo': 'Crear Usuario'})

@login_required
@user_passes_test(es_admin, login_url='home')
def editar_usuario(request, pk):
    """Edita un usuario existente"""
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado')
            return redirect('lista_usuarios')
        
        else:
            # 🔹 AGREGA ESTO (para mostrar errores)
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UsuarioUpdateForm(instance=usuario)
    return render(request, 'usuarios/form_usuario.html', {'form': form, 'titulo': 'Editar Usuario'})

@login_required
@user_passes_test(es_admin, login_url='home')
def eliminar_usuario(request, pk):
    """Elimina un usuario"""
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado')
        return redirect('lista_usuarios')
    return render(request, 'usuarios/confirmar_eliminacion.html', {'usuario': usuario})