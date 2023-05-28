import random

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


def create_fact(request):
    # Verificamos si se envió el formulario
    if request.method == 'POST':
        # Creamos el formulario con los datos del POST
        form = FactForm(request.POST)
        # Verificamos si el formulario es válido
        if form.is_valid():
            # Guardamos el formulario
            form.save()
            # Redireccionamos a la página principal
            return redirect('home')
    else:
        # Creamos el formulario
        form = FactForm()
    # Creamos el contenido de la respuesta
    context = {'form': form}
    # Creamos la respuesta
    return render(request, 'facts/create_fact.html', context=context)
