import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from .forms import FactForm
from .models import Fact


def home(request):
    # Seleccionamos un hecho aleatorio
    current_fact = random.choice(Fact.objects.all())
    # Creamos el contenido de la respuesta
    context = {'current_fact': current_fact}
    # Creamos la respuesta
    return render(request, 'facts/home.html', context=context)


@login_required(login_url='/login/')
def create_fact(request):
    # Verificamos si se envió el formulario
    if request.method == 'POST':
        # Creamos el formulario con los datos del POST
        form = FactForm(request.POST)
        # Verificamos si el formulario es válido
        if form.is_valid():
            # Creamos el objeto sin guardarlo en la base de datos
            fact = form.save(commit=False)
            # Asignamos el usuario autenticado
            fact.user = request.user
            # Guardamos el objeto en la base de datos
            fact.save()
            # Redireccionamos a la página principal
            return redirect('/')
    else:
        # Creamos el formulario
        form = FactForm()
    # Creamos el contenido de la respuesta
    context = {'form': form}
    # Creamos la respuesta
    return render(request, 'facts/create_fact.html', context=context)


def login_view(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('home')
    # Verificamos si se envió el formulario
    if request.method == 'POST':
        # Creamos el formulario con los datos del POST
        form = AuthenticationForm(request, data=request.POST)
        # Verificamos si el formulario es válido
        if form.is_valid():
            # Autenticamos al usuario
            user = form.get_user()
            login(request, user)
            # Obtenemos la URL a la que se debe redireccionar
            redirect_to = request.GET.get('next', '')
            # Redireccionamos a la página principal o a la URL
            return redirect(redirect_to or '/')
    else:
        # Creamos el formulario
        form = AuthenticationForm(request)
    # Creamos la respuesta
    return render(request, 'facts/login.html', {'form': form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('/')
    # Verificamos si se envió el formulario
    if request.method == 'POST':
        # Creamos el formulario con los datos del POST
        form = UserCreationForm(request.POST)
        # Verificamos si el formulario es válido
        if form.is_valid():
            # Guardamos el formulario
            form.save()
            # Redireccionamos a la página de inicio de sesión
            return redirect('/login/')
    else:
        # Creamos el formulario
        form = UserCreationForm()
    # Creamos la respuesta
    return render(request, 'facts/register.html', {'form': form})
