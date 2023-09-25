# Unidad 2: Framework Backend (Parte 2)

Construye aplicaciones web usando un framework del lado del servidor según requerimiento.

## Paso a paso

En la unidad anterior, agregamos un modelo a nuestra aplicación, e incluimos el uso de contenido estático y plantillas. El proyecto resultante quedó con la siguiente estructura:

```plaintext
chuck_norris/
├── chuck_norris/
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── __init__.py
├── facts/
│ ├── migrations/
│ │ ├── __init__.py
│ │ ├── 0001_initial.py
│ │ └── 0002_initial_data.py
│ ├── static/
│ │ └── facts/
│ │   └── css/
│ │     └── styles.css
│ ├── templates/
│ │ └── facts/
│ │   ├── 404.html
│ │   ├── base.html
│ │   ├── create.html
│ │   ├── detail.html
│ │   ├── home.html
│ │   └── random.html
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ ├── views.py
│ └── __init__.py
└── manage.py
```

Como primer paso, vamos a incorporar el uso de sesiones en nuestra aplicación, para asegurarnos que, al momento de mostrar un hecho aleatorio, este no se repita. Para ello, vamos a modificar el archivo `views.py` de la aplicación `facts`:

```python
import random
from django.shortcuts import render
from .forms import FactForm
from .models import Fact

def home_view(request):
    ...

def fact_view(request, fact_id):
    ...

def random_view(request):
    # Obtiene la lista de hechos vistos (identificadores únicos)
    seen_facts_ids = request.session.get('seen_facts_ids', [])
    # Filtra la lista de hechos para mostrar solo los que el
    # usuario aún no ha visto (por identificador único)
    remaining_facts = Fact.objects.exclude(id__in=seen_facts_ids)
    # Si no quedan hechos por mostrar, reinicia la lista
    if not remaining_facts:
        # Si el usuario ha visto todos los hechos,
        # reinicia la lista
        seen_facts_ids = []
        remaining_facts = Fact.objects.all()
    # Elige un hecho aleatorio de los que quedan por mostrar
    current_fact = random.choice(remaining_facts)
    # Agrega el identificador único del hecho actual a la lista
    # de hechos vistos por el usuario
    seen_facts_ids.append(current_fact.id)
    # Almacena la lista actualizada de hechos vistos en la
    # sesión del usuario
    request.session['seen_facts_ids'] = seen_facts_ids
    # Creamos el contenido de la respuesta
    context = {'fact': current_fact}
    # Creamos la respuesta
    return render(request, 'facts/random.html', context=context)

def create_fact(request):
    ...
```

Aquí está la explicación detallada del funcionamiento del código:

1. Se obtiene la lista de identificadores únicos de hechos vistos del objeto de sesión del usuario. Estos identificadores se almacenan en la clave `'seen_facts_ids'` de la sesión. Si la clave no existe en la sesión, se utiliza una lista vacía como valor predeterminado.

2. Se filtra la lista de hechos utilizando el método `exclude` de Django para mostrar solo los hechos que el usuario aún no ha visto. Esto se hace utilizando la función `exclude(id__in=seen_facts_ids)`, que excluye los hechos cuyos identificadores estén en la lista `seen_facts_ids`.

3. Si no quedan hechos por mostrar (es decir, `remaining_facts` está vacío), se reinicia la lista `seen_facts_ids` a una lista vacía y se obtienen todos los hechos disponibles.

4. Se elige un hecho aleatorio de la lista de hechos que aún no se han visto utilizando la función `random.choice`. Esto selecciona aleatoriamente un elemento de la lista `remaining_facts` y lo almacena en la variable `current_fact`.

5. Se agrega el identificador único del hecho actual (`current_fact.id`) a la lista `seen_facts_ids`, lo que indica que el usuario ha visto este hecho.

6. Se actualiza la lista de identificadores de hechos vistos en la sesión del usuario, almacenándola en `request.session['seen_facts_ids']`.

7. Se crea un contexto (`context`) que contiene el hecho aleatorio seleccionado (`current_fact`). Este contexto se utilizará para renderizar la plantilla HTML.

8. Finalmente, se renderiza la plantilla `'facts/random.html'` utilizando la función `render`, pasando el objeto `request` y el contexto `context` como argumentos. Esto devuelve una respuesta HTTP que muestra el hecho aleatorio al usuario.

Ahora vamos a agregar seguridad a nuestra aplicación. Para ello, vamos a utilizar el sistema de autenticación de Django.

Para lograr lo anterior, lo primero es crear las plantillas que se usarán posteriormente. La primera plantilla que vamos a crear se llama `login.html`, y se encuentra en el directorio `templates/facts`:

```html
{% extends 'facts/base.html' %} {% load bootstrap5 %} {% block title %}Iniciar
sesión{% endblock %} {% block content %}
<h1 class="text-center">Iniciar sesión</h1>
<form method="POST">
  {% csrf_token %} {% bootstrap_form form layout='horizontal' %}
  <button type="submit" class="btn btn-lg btn-primary fw-bold">
    Iniciar sesión
  </button>
</form>
{% endblock %}
```

La segunda plantilla que vamos a crear se llama `register.html`, y se encuentra en el directorio `templates/facts`:

```html
{% extends 'facts/base.html' %} {% load bootstrap5 %} {% block title
%}Registrarse{% endblock %} {% block content %}
<h1 class="text-center">Registrarse</h1>
<form method="POST">
  {% csrf_token %} {% bootstrap_form form layout='horizontal' %}
  <button type="submit" class="btn btn-lg btn-primary fw-bold">
    Crear usuario
  </button>
</form>
{% endblock %}
```

Una vez creadas las plantillas, modificaremos el archivo `models.py` de la aplicación `facts` para agregar un nuevo campo al modelo `Fact`, llamado `user`, que será una referencia al modelo `User` de Django:

```python
from django.contrib.auth.models import User
from django.db import models

class Fact(models.Model):
    fact = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.fact
```

Lo anterior permitirá que cada vez que se cree un nuevo hecho, se asigne el usuario que lo creó.

Para que los cambios en el modelo se vean reflejados en la base de datos, debemos ejecutar las migraciones correspondientes:

```bash
python manage.py makemigrations
python manage.py migrate
```

Ahora es el turno de modificar el archivo `views.py` de la aplicación `facts`. El primer paso es importar las clases `AuthenticationForm` y `UserCreationForm` desde el módulo `django.contrib.auth.forms`. También vamos a importar las funciones `login` y `logout` desde el módulo `django.contrib.auth`. Finalmente, vamos a importar el decorador `login_required` desde el módulo `django.contrib.auth.decorators`, y `redirect` desde el módulo `django.shortcuts`.

Con el paso anterior listo, crearemos las vistas necesarias para iniciar sesión, cerrar sesión y registrarse, llamadas `login_view`, `logout_view` y `register_view`, respectivamente. También modificaremos la vista `create_view` para que solo los usuarios autenticados puedan crear nuevos hechos.

El archivo `views.py` de la aplicación `facts` queda de la siguiente manera:

```python
import random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from .forms import FactForm
from .models import Fact

def home_view(request):
    ...

def fact_view(request, fact_id):
    ...

def random_view(request):
    ...

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
```

Veamos algunos puntos interesantes del código anterior:

- La función `redirect` es una utilidad que se utiliza para redirigir a los usuarios a una URL específica después de que se ha realizado una acción o procesamiento en una vista. Esta función es útil cuando deseas redirigir al usuario a una página diferente después de completar una operación, como enviar un formulario o realizar alguna otra acción. Toma dos argumentos principales:
  - `to`: Es la URL a la que se debe redirigir al usuario. Puede ser una URL absoluta (completa) o una URL relativa en forma de cadena.
  - `permanent` (opcional): Especifica si la redirección debe ser permanente o no. Si se omite, se utiliza una redirección temporal.
- La función `login` se utiliza para agregar a un usuario en la sesión actual, después de que ha proporcionado sus credenciales y ha sido autenticado. Esto le permite acceder a las áreas protegidas y realizar acciones como usuario autenticado. Toma tres argumentos principales:
  - `request`: Es el objeto de solicitud de Django, que se utiliza para gestionar la sesión del usuario.
  - `user`: Es el objeto de usuario que deseas autenticar en la sesión actual. Este objeto debe ser un usuario válido que haya sido previamente autenticado por medio de sus credenciales.
  - `backend` (opcional): Especifica el _back end_ de autenticación que se utilizará para autenticar al usuario. Si se omite, se utiliza el _back end_ de autenticación predeterminado.
- La función `logout` se utiliza para cerrar la sesión de un usuario autenticado en la aplicación web. Esto elimina la información de autenticación de la sesión actual y redirige al usuario a la página de inicio de sesión o a otra página específica, dependiendo de la configuración de la aplicación. Toma un argumento principal:
  - `request`: Es el objeto de solicitud de Django, que se utiliza para gestionar la sesión del usuario.
- El decorador `@login_required` permite proteger las vistas de tu aplicación web, asegurándose de que solo los usuarios autenticados tengan acceso a ellas. Si un usuario intenta acceder a una vista decorada con `@login_required` sin haber iniciado sesión previamente, se le redirige automáticamente a la página de inicio de sesión o a otra página específica definida en la configuración o los parámetros, para autenticarse antes de permitir el acceso a la vista deseada. Este decorador admite algunos parámetros que te permiten personalizar su comportamiento:
  - `login_url` (opcional): Este parámetro te permite especificar la URL a la que se redirigirá a los usuarios no autenticados. Si no se proporciona, se utiliza la URL de inicio de sesión predeterminada definida en la configuración de Django (`LOGIN_URL` en `settings.py`).
  - `redirect_field_name` (opcional): Este parámetro te permite especificar el nombre del campo que se utilizará para almacenar la URL original a la que el usuario intentaba acceder antes de ser redirigido a la página de inicio de sesión. Por defecto, se utiliza el valor `next`.
  - `login_url_required` (opcional): Si se establece en `True`, el decorador `login_required` solo permitirá el acceso a la vista si el usuario ha sido redirigido desde la página de inicio de sesión. Esto puede ser útil cuando se necesita controlar que el acceso a una vista específica solo se realice después de iniciar sesión, y no si el usuario simplemente ingresa la URL manualmente.

Ahora es el turno de modificar el archivo `settings.py` para agregar la configuración de autenticación. Para ello, debemos agregar las siguientes líneas al final del archivo:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

Para que Django reconozca las nuevas vistas, debemos modificar el archivo `urls.py` de la aplicación `facts`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('<int:fact_id>/', views.fact_view, name='fact'),
    path('random/', views.random_view, name='random'),
    path('create/', views.create_view, name='create'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
```

Por último, modificaremos el archivo `base.html` de la aplicación `facts` para agregar un menú de navegación:

```html
...
<body class="d-flex h-100 text-center text-white bg-dark">
    <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
        <header class="mb-auto">
            <div>
                <h3 class="float-md-start mb-0">Hechos de Chuck Norris</h3>
                <nav class="nav nav-masthead justify-content-center float-md-end">
                    <a class="nav-link" href="{% url 'home' %}">
                        Inicio
                    </a>
                    <a class="nav-link" href="{% url 'random' %}">
                        Aleatorio
                    </a>
                    {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'create_fact' %}">
                        Nuevo
                    </a>
                    <span class="dropdown">
                        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown"
                           href="#" role="button" aria-expanded="false">
                            {{ user.username }}
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <a class="dropdown-item" href="{% url 'logout' %}">
                                    Cerrar sesión
                                </a>
                            </li>
                        </ul>
                    </span>
                    {% else %}
                    <a class="nav-link" href="{% url 'login' %}">
                        Iniciar sesión
                    </a>
                    <a class="nav-link" href="{% url 'register' %}">
                        Registrarse
                    </a>
                    {% endif %}
                </nav>
            </div>
        </header>
        ...
</body>
...
```

Con la seguridad implementada y el modelo actualizado, podemos probar nuestra aplicación. Para ello, vamos a ejecutar el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

Ahora, podemos ingresar a la URL [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) para ver el resultado.
