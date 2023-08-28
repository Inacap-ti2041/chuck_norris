import random

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
    # Seleccionamos un hecho aleatorio
    current_fact = random.choice(Fact.objects.all())
    # Creamos el contenido de la respuesta
    context = {'fact': current_fact}
    # Creamos la respuesta
    return render(request, 'facts/random.html', context=context)


def create_view(request):
    # Verificamos si se envió el formulario
    if request.method == 'POST':
        # Creamos el formulario con los datos del POST
        form = FactForm(request.POST)
        # Verificamos si el formulario es válido
        if form.is_valid():
            # Guardamos el formulario
            new_fact = form.save()
            # Redireccionamos a la página de detalle
            return redirect('fact', fact_id=new_fact.id)
    else:
        # Creamos el formulario
        form = FactForm()
    # Creamos el contenido de la respuesta
    context = {'form': form}
    # Creamos la respuesta
    return render(request, 'facts/create.html', context=context)
