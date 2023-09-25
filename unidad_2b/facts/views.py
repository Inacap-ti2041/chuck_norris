import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from .forms import FactForm
from .models import Fact


def home_view(request):
    # Creamos el contenido de la respuesta
    context = {'facts': Fact.objects.all()}
    # Creamos la respuesta
    return render(request, 'facts/home.html', context=context)


def fact_view(request, fact_id):
    try:
        # Seleccionamos un hecho específico
        current_fact = Fact.objects.get(id=fact_id)
        # Creamos el contenido de la respuesta
        context = {'fact': current_fact}
        # Creamos la respuesta
        return render(request, 'facts/detail.html', context=context)
    except Fact.DoesNotExist:
        # Creamos la respuesta
        return render(request, 'facts/404.html', status=404)


def random_view(request):
    # Obtiene la lista de hechos vistos (identificadores únicos)
    seen_facts_ids = request.session.get('seen_facts_ids', [])
    # Filtra la lista de hechos para mostrar solo los que el
    # usuario aún no ha visto (por identificador único)
    remaining_facts = Fact.objects.exclude(id__in=seen_facts_ids)
    # Si no quedan hechos por mostrar, reinicia la lista
    if not remaining_facts:
        # Si el usuario ha visto todos los hechos, reinicia la lista
        seen_facts_ids = []
        remaining_facts = Fact.objects.all()
    # Elige un hecho aleatorio de los que quedan por mostrar
    current_fact = random.choice(remaining_facts)
    # Agrega el identificador único del hecho actual a la lista
    # de hechos vistos por el usuario
    seen_facts_ids.append(current_fact.id)
    # Almacena la lista actualizada de hechos vistos en la sesión del usuario
    request.session['seen_facts_ids'] = seen_facts_ids
    # Creamos el contenido de la respuesta
    context = {'fact': current_fact}
    # Creamos la respuesta
    return render(request, 'facts/random.html', context=context)


@login_required
def create_view(request):
    # Verificamos si se envió el formulario
    if request.method == 'POST':
        # Creamos el formulario con los datos del POST
        form = FactForm(request.POST)
        # Verificamos si el formulario es válido
        if form.is_valid():
            # Creamos el objeto sin guardarlo en la base de datos
            new_fact = form.save(commit=False)
            # Asignamos el usuario autenticado
            new_fact.user = request.user
            # Guardamos el objeto en la base de datos
            new_fact.save()
            # Redireccionamos a la página de detalle
            return redirect('fact', fact_id=new_fact.id)
    else:
        # Creamos el formulario
        form = FactForm()
    # Creamos el contenido de la respuesta
    context = {'form': form}
    # Creamos la respuesta
    return render(request, 'facts/create.html', context=context)


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
            redirect_to = request.GET.get('next', '/facts/')
            # Redireccionamos a la página principal o a la URL
            return redirect(redirect_to)
    else:
        # Creamos el formulario
        form = AuthenticationForm(request)
    # Creamos la respuesta
    return render(request, 'facts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/facts/')


def register_view(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('/facts/')
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
