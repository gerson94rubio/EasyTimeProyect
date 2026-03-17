#se modifico aca para que al cerrar la pagina no vuelva a entrar inicio de secion con el usuario anterior
#tambien se mofifio base tlm ose inicio de secion colocamos un post y urls py 


from django.shortcuts import render, redirect
from django.contrib.auth import logout

def home(request):
    return render(request, 'home.html')

def custom_logout(request):
    logout(request)
    return redirect('home')