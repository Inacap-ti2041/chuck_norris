# Unidad 2: Framework Backend (Parte 2)

Construye aplicaciones web usando un framework del lado del servidor según requerimiento.

## Paso a paso

En la unidad anterior, agregamos el modelo a nuestro aplicación. El proyecto resultante quedó con la siguiente estructura:

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
│ ├── templates/
│ │ └── facts/
│ │   ├── base.html
│ │   ├── create_fact.html
│ │   └── home.html
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

Ahora vamos a incorporar un poco de seguridad a nuestra aplicación. Para ello, vamos a agregar un formulario de autenticación para que los usuarios puedan ingresar a la aplicación.

El primer paso es crear una vista para que los usuarios puedan iniciar sesión en nuestra aplicación. Para ello, vamos a crear una vista llamada `login_view` en el archivo `views.py` de la aplicación `facts`:

```python
import random
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from .forms import FactForm
from .models import Fact

def home(request):
    ... # Código omitido para mantener el ejemplo corto

def create_fact(request):
    ... # Código omitido para mantener el ejemplo corto

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
```

Luego, vamos a crear una plantilla para que los usuarios puedan iniciar sesión en nuestra aplicación. Para ello, vamos a crear una plantilla llamada `login.html` en el directorio `templates/facts`:

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

Luego, vamos a crear una URL para que los usuarios puedan iniciar sesión en nuestra aplicación. Para ello, vamos a crear una URL llamada `login` en el archivo `urls.py` de la aplicación `facts`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_fact, name='create_fact'),
    path('login/', views.login_view, name='login'),
]
```

Ahora, vamos a crear una vista para que los usuarios puedan cerrar sesión en nuestra aplicación. Para ello, vamos a crear una vista llamada `logout_view` en el archivo `views.py` de la aplicación `facts`:

```python
import random
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from .forms import FactForm
from .models import Fact

def home(request):
    ... # Código omitido para mantener el ejemplo corto

def create_fact(request):
    ... # Código omitido para mantener el ejemplo corto

def login_view(request):
    ... # Código omitido para mantener el ejemplo corto

def logout_view(request):
    logout(request)
    return redirect('/')
```

Luego, vamos a crear una URL para que los usuarios puedan cerrar sesión en nuestra aplicación. Para ello, vamos a crear una URL llamada `logout` en el archivo `urls.py` de la aplicación `facts`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_fact, name='create_fact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

Ahora, vamos a crear una vista para que los usuarios puedan registrarse en nuestra aplicación. Para ello, vamos a crear una vista llamada `register_view` en el archivo `views.py` de la aplicación `facts`:

```python
import random
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from .forms import FactForm
from .models import Fact

def home(request):
    ... # Código omitido para mantener el ejemplo corto

def create_fact(request):
    ... # Código omitido para mantener el ejemplo corto

def login_view(request):
    ... # Código omitido para mantener el ejemplo corto

def logout_view(request):
    ... # Código omitido para mantener el ejemplo corto

def register_view(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('home')
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

Luego, vamos a crear una plantilla para que los usuarios puedan registrarse en nuestra aplicación. Para ello, vamos a crear una plantilla llamada `register.html` en el directorio `templates/facts`:

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

Ahora es el turno de crear una URL para que los usuarios puedan registrarse en nuestra aplicación. Para ello, vamos a crear una URL llamada `register` en el archivo `urls.py` de la aplicación `facts`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_fact, name='create_fact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
```

En este momento, estamos en posición de proteger las vistas de nuestra aplicación. Para ello, vamos a decorar la vista `create_fact` con el decorador `login_required`:

```python
import random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from .forms import FactForm
from .models import Fact

def home(request):
    ... # Código omitido para mantener el ejemplo corto

@login_required(login_url='/login/')
def create_fact(request):
    ... # Código omitido para mantener el ejemplo corto

def login_view(request):
    ... # Código omitido para mantener el ejemplo corto

def logout_view(request):
    ... # Código omitido para mantener el ejemplo corto

def register_view(request):
    ... # Código omitido para mantener el ejemplo corto
```

Lo anterior nos permite que las vistas marcadas con el decorador solo puedan ser accedidas por usuarios autenticados. En caso de que un usuario no autenticado intente acceder a estas vistas, será redireccionado a la vista `login_view`.

El modelo `User` de Django nos permite obtener la información de un usuario autenticado, e incluirla como parte del modelo `Fact`. Para ello, vamos a modificar el archivo `models.py` de la aplicación `facts`. Hay que tener en consideración que, al modificar el modelo, debemos indicar el valor por defecto de los registros existentes. Para ello, vamos a utilizar el valor `1` para el campo `user`:

```python
from django.db import models
from django.contrib.auth.models import User

class Fact(models.Model):
    ... # Código omitido para mantener el ejemplo corto
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
```

Ahora, debemos generar la migración para aplicar los cambios en la base de datos:

```bash
python manage.py makemigrations fact
python manage.py migrate
```

Luego, vamos a modificar la vista `create_fact` para que el usuario autenticado sea asignado al campo `user` del modelo `Fact`. Para ello, vamos a modificar el archivo `views.py` de la aplicación `facts`:

```python
import random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from .forms import FactForm
from .models import Fact

def home(request):
    ... # Código omitido para mantener el ejemplo corto

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
            # Redireccionamos a la página de inicio
            return redirect('/')
    else:
        # Creamos el formulario
        form = FactForm()
    # Creamos la respuesta
    return render(request, 'facts/create_fact.html', {'form': form})

def login_view(request):
    ... # Código omitido para mantener el ejemplo corto

def logout_view(request):
    ... # Código omitido para mantener el ejemplo corto

def register_view(request):
    ... # Código omitido para mantener el ejemplo corto
```

Y ahora, con la seguridad implementada y el modelo actualizado, podemos probar nuestra aplicación. Para ello, vamos a ejecutar el servidor de desarrollo de Django:

```bash
python manage.py runserver
```
