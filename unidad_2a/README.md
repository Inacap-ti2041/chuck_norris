# Unidad 2: Framework Backend (Parte 1)

Construye aplicaciones web usando un framework del lado del servidor según requerimiento.

## Paso a paso

En la unidad anterior, creamos un proyecto Django y una aplicación. El proyecto resultante quedó con la siguiente estructura:

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
│ │ └── __init__.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ ├── views.py
│ └── __init__.py
└── manage.py
```

Ahora, vamos a crear un modelo para almacenar los datos de los hechos de Chuck Norris.

En primer lugar, debemos definir el modelo. Para ello, modificaremos el archivo `models.py` de la aplicación `facts`:

```python
from django.db import models

class Fact(models.Model):
    fact = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fact
```

En el código anterior, definimos un modelo llamado `Fact` que tiene tres atributos: `fact`, `created_at` y `updated_at`. El primero es un campo de texto que almacena el hecho de Chuck Norris. Los otros dos campos son de tipo fecha y hora, y se utilizan para almacenar la fecha y hora de creación y actualización del registro. También definimos un método `__str__` que retorna el valor del atributo `fact` cuando se imprime el objeto.

Ahora, debemos crear la migración para que Django cree la tabla en la base de datos. Para ello, ejecutaremos el siguiente comando:

```bash
python manage.py makemigrations facts
```

Con la migración creada, debemos ejecutarla para que se cree la tabla en la base de datos. Para ello, ejecutaremos el siguiente comando:

```bash
python manage.py migrate
```

Ahora, podemos crear los registros iniciales en la base de datos. Para ello, vamos a crear una migración de datos. Para ello, ejecutaremos el siguiente comando:

```bash
python manage.py makemigrations facts --empty --name initial_data
```

En el archivo de migración creado (`initial_data.py`), agregaremos el siguiente código:

```python
from django.db import migrations

def create_facts(apps, schema_editor):
    Fact = apps.get_model('facts', 'Fact')
    Fact.objects.create(fact='Chuck Norris puede dividir entre cero.')
    ... # Agregar más hechos
    Fact.objects.create(fact="La gente usa pijamas de Superman. Superman usa pijamas de Chuck Norris.")

class Migration(migrations.Migration):

        dependencies = [
            ('facts', '0001_initial'),
        ]

        operations = [
            migrations.RunPython(create_facts),
        ]
```

En el código anterior, definimos una función llamada `create_facts` que crea los registros iniciales en la base de datos. Luego, en la clase `Migration`, definimos una operación que ejecuta la función `create_facts`.

Ahora, debemos ejecutar la migración de datos usando el comando:

```bash
python manage.py migrate
```

Con esto, ya tenemos creada la tabla en la base de datos y los registros iniciales.

Ahora, vamos a crear una vista para mostrar los hechos de Chuck Norris. Para ello, modificaremos el archivo `views.py` de la aplicación `facts`:

```python
import random
from django.shortcuts import render
from .models import Fact

def home(request):
    # Seleccionamos un hecho aleatorio
    current_fact = random.choice(Fact.objects.all())
    # Creamos el contenido de la respuesta
    context = {'current_fact': current_fact}
    # Creamos la respuesta
    return render(request, 'facts/home.html', context=context)
```

En el código anterior, definimos una función llamada `home` que selecciona un hecho aleatorio de la base de datos y lo muestra en la página principal. Luego, creamos el contenido de la respuesta. Finalmente, creamos la respuesta usando el método `render` de Django.

Ahora, debemos crear la plantilla para mostrar el hecho de Chuck Norris. Para ello, crearemos el archivo `home.html` en la carpeta `templates/facts`, dentro de la aplicación `facts`:

```html
{% extends 'facts/base.html' %} {% block title %}Hechos de Chuck Norris{%
endblock %} {% block content %}
<h1>Hechos de Chuck Norris</h1>
<p class="lead">{{ current_fact }}</p>
<p class="lead">
  <a
    href="{% url 'create_fact' %}"
    class="btn btn-lg btn-secondary fw-bold border-white bg-white"
  >
    Nuevo hecho
  </a>
</p>
{% endblock %}
```

En el código anterior, definimos un bloque `content` que muestra el hecho de Chuck Norris. También definimos un bloque `title` que define el título de la página.

Ahora, debemos definir el archivo `base.html` que define la plantilla base de la aplicación. Para ello, crearemos el archivo `base.html` en la carpeta `templates`, dentro de la aplicación `facts`:

```html
<!DOCTYPE html>
<html lang="es" class="h-100">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}{% endblock %}</title>
    {% load bootstrap5 %} {% bootstrap_css %}
    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }

      /*
        * Globals
        */

      /* Custom default button */
      .btn-secondary,
      .btn-secondary:hover,
      .btn-secondary:focus {
        color: #333;
        text-shadow: none;
        /* Prevent inheritance from `body` */
      }

      /* Base structure */
      body {
        text-shadow: 0 0.05rem 0.1rem rgba(0, 0, 0, 0.5);
        box-shadow: inset 0 0 5rem rgba(0, 0, 0, 0.5);
      }

      .cover-container {
        max-width: 42em;
      }

      /* Header */
      .nav-masthead .nav-link {
        padding: 0.25rem 0;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.5);
        background-color: transparent;
        border-bottom: 0.25rem solid transparent;
      }

      .nav-masthead .nav-link:hover,
      .nav-masthead .nav-link:focus {
        border-bottom-color: rgba(255, 255, 255, 0.25);
      }

      .nav-masthead .nav-link + .nav-link {
        margin-left: 1rem;
      }

      .nav-masthead .active {
        color: #fff;
        border-bottom-color: #fff;
      }
    </style>
  </head>
  <body class="d-flex h-100 text-center text-white bg-dark">
    <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
      <header class="mb-auto">
        <div>
          <h3 class="float-md-start mb-0">Hechos de Chuck Norris</h3>
          <nav class="nav nav-masthead justify-content-center float-md-end">
            <a class="nav-link" href="{% url 'home' %}">Inicio</a>
            <a class="nav-link" href="{% url 'create_fact' %}">Nuevo</a>
          </nav>
        </div>
      </header>
      <main class="px-3">{% block content %}{% endblock %}</main>
      <footer class="mt-auto text-white-50">
        <p>
          Proyecto creado por
          <a href="mailto:jose.candia07@inacapmail.cl" class="text-white"
            >José Miguel Candia</a
          >, para la asignatura Programación Back End.
        </p>
      </footer>
    </div>
    {% bootstrap_javascript %}
  </body>
</html>
```

En el código anterior, definimos un bloque `content` que define el contenido de la página. También definimos un bloque `title` que define el título de la página. Además, agregamos los enlaces a los archivos CSS y JavaScript de Bootstrap.

Hasta este punto, tenemos creada la vista para mostrar los hechos de Chuck Norris. Ahora, debemos crear el formulario para crear nuevos hechos de Chuck Norris. Para ello, crearemos el archivo `forms.py` en la carpeta `facts`, dentro de la aplicación `facts`:

```python
from django import forms
from .models import Fact

class FactForm(forms.ModelForm):
    class Meta:
        model = Fact
        fields = ['fact']
        widgets = {
            'fact': forms.Textarea
        }
        labels = {
            'fact': 'Hecho'
        }
```

En el código anterior, definimos una clase llamada `FactForm` que hereda de `forms.ModelForm`. Luego, definimos una clase `Meta` que define el modelo y los campos del formulario. Además, definimos un widget para el campo `fact` que define que el campo es un `Textarea`. Por último, definimos una etiqueta para el campo `fact` que define el texto que se mostrará en el formulario.

Ahora, debemos definir la vista para crear nuevos hechos. Para ello, modificaremos el archivo `views.py` de la aplicación `facts`:

```python
from django.shortcuts import render, redirect
from .models import Fact
from .forms import FactForm

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
```

En el código anterior, definimos una función llamada `create_fact` que crea un nuevo hecho de Chuck Norris. Luego, creamos el contenido de la respuesta. Finalmente, creamos la respuesta usando el método `render` de Django.

Ahora, debemos crear la plantilla para crear nuevos hechos de Chuck Norris. Para ello, crearemos el archivo `create_fact.html` en la carpeta `templates/facts`, dentro de la aplicación `facts`:

```html
{% extends 'facts/base.html' %} {% load bootstrap5 %} {% block title %}Crear
nuevo hecho{% endblock %} {% block content %}
<h1>Crear nuevo hecho</h1>
<form action="{% url 'create_fact' %}" method="POST">
  {% csrf_token %} {% bootstrap_form form layout='horizontal' %}
  <button type="submit" class="btn btn-lg btn-primary fw-bold">Crear</button>
</form>
{% endblock %}
```

En el código anterior, definimos un bloque `content` que muestra el formulario para crear nuevos hechos de Chuck Norris. También definimos un bloque `title` que define el título de la página.

Las plantillas anteriores usan la librearía `django-bootstrap-v5` para mostrar los formularios de Django usando Bootstrap. Para instalar esta librería, ejecutaremos el siguiente comando:

```bash
pip install django-bootstrap-v5
```

Y agregaremos la librería a la lista de aplicaciones instaladas en el archivo `settings.py`, en la sección `INSTALLED_APPS` de la siguiente forma:

```python
INSTALLED_APPS = [
    ...
    'bootstrap5',
    ...
]
```

Ahora, debemos definir la URL para crear nuevos hechos de Chuck Norris. Para ello, modificaremos el archivo `urls.py` de la aplicación `facts`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_fact, name='create_fact'),
]
```

En el código anterior, definimos la URL para crear nuevos hechos de Chuck Norris. Para ello, definimos la ruta `create/` que apunta a la función `create_fact` de la aplicación `facts`.

En este punto, podemos ejecutar el servidor de desarrollo de Django para probar la aplicación:

```bash
python manage.py runserver
```

Como paso adicional, podemos incorporar el modelo `Fact` al panel de administración de Django. Para ello, modificaremos el archivo `admin.py` de la aplicación `facts`:

```python
from django.contrib import admin
from .models import Fact

class FactAdmin(admin.ModelAdmin):
    list_display = ('fact', 'created_at', 'updated_at')

admin.site.register(Fact)
```

En el código anterior, definimos una clase `FactAdmin` que define los campos que se mostrarán en el panel de administración. Luego, registramos el modelo `Fact` para que se pueda administrar desde el panel de administración, junto con la clase `FactAdmin`, que define los campos que se mostrarán.

Para poder administrar el modelo `Fact` desde el panel de administración, debemos crear un superusuario. Para ello, ejecutaremos el siguiente comando:

```bash
python manage.py createsuperuser
```

Luego, debemos ingresar un nombre de usuario, una dirección de correo electrónico y una contraseña. Una vez que hayamos creado el superusuario, podemos iniciar el servidor de desarrollo de Django para probar la aplicación:

```bash
python manage.py runserver
```

Ahora, podemos ingresar a la URL [http://localhost:8000/admin/](http://localhost:8000/admin/) para ingresar al panel de administración. Luego, debemos ingresar las credenciales del superusuario que creamos anteriormente. Una vez que hayamos ingresado al panel de administración, podemos administrar los hechos de Chuck Norris.
