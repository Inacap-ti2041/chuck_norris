# Unidad 1: Tecnologías del lado del servidor

Realiza programa del lado del servidor, de acuerdo a la sintaxis del lenguaje.

## Paso a paso

En primer lugar, crearemos la carpeta donde alojaremos el proyecto. Para ello, ejecutaremos el siguiente comando:

```bash
mkdir chuck_norris
```

Luego, debemos acceder al directorio:

```bash
cd chuck_norris
```

Una vez dentro, crearemos el proyecto en Django con el siguente comando:

```bash
django-admin startproject chuck_norris .
```

> **Nota:** Es importante destacar el punto al final del comando. Ese parámetro le indica a Django que debe crear el proyecto en el primer nivel del directorio.

Con el projecto Django creado, ahora debemos crear la aplicación. Para lograrlo, ejecutaremos el siguiente comando:

```bash
python manage.py startapp facts
```

Con lo anterior completamente ejecutado, podemos observar la siguiente estructura dentro del directorio:

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
│ ├── views.py
│ └── __init__.py
└── manage.py
```

Ahora es el turno de configurar el proyecto, para que reconozca la aplicación creada. Para ello, modificaremos la sección `INSTALLED_APPS` del archivo `settings.py` que se encuentra en la carpeta `chuck_norris`.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'facts', # <- Esta es la aplicación creada
]
```

También podemos hacer otras modificaciones en el archivo `settings.py`, como modificar la zona horaria o el lenguaje de Django:

```python
LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True
```

Con todo configurado, es momento de empezar a desarrollar nuestra aplicación. El primer paso es modificar el archivo `views.py` de la carpeta `facts`.

```python
from django.shortcuts import HttpResponse
import random

# Lista de hechos de Chuck Norris
FACTS_LIST = [
    {
        'id': 1,
        'fact': 'Chuck Norris contó hasta el infinito. Dos veces.'
    },
    {
        'id': 2,
        'fact': 'Chuck Norris puede dividir por cero.'
    },
    {
        'id': 3,
        'fact': 'Chuck Norris puede reproducir un CD en un tocadiscos.'
    },
    {
        'id': 4,
        'fact': 'Chuck Norris puede ganar al Sol en un juego de miradas.'
    },
    {
        'id': 5,
        'fact': 'Chuck Norris dona sangre a menudo. Pero rara vez es la suya.'
    }
]

def home_view(request):
    # Creamos la tabla de hechos
    facts_table = '<ul>'
    for fact in FACTS_LIST:
        facts_table += f'<li><a href="/facts/{fact["id"]}">Hecho {fact["id"]}</a></li>'
    facts_table += '</ul>'
    # Creamos el contenido de la respuesta
    content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chuck Norris</title>
    </head>
    <body>
        <p>Hechos de Chuck Norris</p>
        <blockquote>{facts_table}</blockquote>
    </body>
    </html>
    '''
    # Creamos la respuesta
    return HttpResponse(content)

def fact_view(request, fact_id):
    try:
        # Seleccionamos un hecho específico
        current_fact = next(
            (fact['fact'] for fact in FACTS_LIST if fact['id'] == fact_id))
        # Creamos el contenido de la respuesta
        content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chuck Norris</title>
        </head>
        <body>
            <p>Este es un hecho de Chuck Norris con ID {fact_id}</p>
            <blockquote>{current_fact}</blockquote>
        </body>
        </html>
        '''
        # Creamos la respuesta
        return HttpResponse(content)
    except StopIteration:
        # En caso de que el ID no exista, se genera la excepción StopIteration,
        # la cual gestionamos con el siguiente código
        content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chuck Norris</title>
        </head>
        <body>
            <p>El hecho con ID {fact_id} no existe</p>
        </body>
        </html>
        '''
        # Creamos la respuesta
        return HttpResponse(content, status=404)

def random_view(request):
    # Seleccionamos un hecho aleatorio
    current_fact = random.choice(FACTS_LIST)
    # Creamos el contenido de la respuesta
    content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chuck Norris</title>
    </head>
    <body>
        <p>Este es un hecho aleatorio de Chuck Norris</p>
        <blockquote>{current_fact['fact']}</blockquote>
    </body>
    </html>
    '''
    # Creamos la respuesta
    return HttpResponse(content)
```

La explicación del código anterior es la siguiente:

- La función llamada `home_view` es la encargada de generar un listado con todos los hechos almacenados en la lista de diccionarios `FACTS_LIST`. La respuesta que se genera es un documento HTML, con un listado de enlaces a cada uno de los hechos.
- La función llamada `fact_view` es la encargada de responder un hecho específico en base al ID que se recibe como parámetro. Para lograrlo, se utiliza la función `next` que recibe como parámetro un generador. Luego, se crea el contenido de la respuesta, el cual es un documento HTML. Finalmente, se retorna la respuesta con el contenido creado. En caso de que el ID no exista, se gestiona la excepción `StopIteration` y se retorna una respuesta con el código de estado 404.
- Por último, la función llamada `random_view` es la encargada de responder un hecho aleatorio. Para lograrlo, se utiliza la función `random.choices`, que se importa del paquete `random`, que recibe como parámetro una lista de elementos y retorna un elemento aleatorio de la lista. Luego, se crea el contenido de la respuesta, el cual es un documento HTML. Finalmente, se retorna la respuesta con el contenido creado.

Cabe resaltar que todas las funciones usan la función `HttpResponse` para crear la respuesta. Esta función recibe como parámetro el contenido de la respuesta y opcionalmente el código de estado de la respuesta. Por defecto, el código de estado es 200.

Ahora debemos crear el archivo `urls.py` en la carpeta `facts`. Este archivo es el encargado de definir las rutas de la aplicación.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('<int:fact_id>/', views.fact_view, name='fact'),
    path('random/', views.random_view, name='random'),
]
```

La explicación del código anterior es la siguiente:

- Se importa la función `path` desde el módulo `django.urls`. Esta función permite definir las rutas de la aplicación.
- Se importa el módulo `views` de la aplicación. Este módulo contiene las funciones que se encargan de generar las respuestas.
- Se define la ruta raíz de la aplicación. Esta ruta se asocia a la función `home_view` de la aplicación.
- Se define la ruta `<int:fact_id>/` de la aplicación. Esta ruta se asocia a la función `fact_view` de la aplicación. Esta ruta recibe como parámetro un ID de tipo entero.
- Se define la ruta `random/` de la aplicación. Esta ruta se asocia a la función `random_view` de la aplicación.

Con las rutas definidas, debemos modificar el archivo `urls.py` de la carpeta `chuck_norris`.

```python
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Establece la ruta para la aplicación de hechos
    path('facts/', include('facts.urls')),
    # Redirecciona la ruta raíz a la ruta de hechos
    path('', RedirectView.as_view(url='/facts/', permanent=True)),
]
```

A continuación, se explica el código anterior:

- La función `include` se importa desde el módulo `django.urls`. Esta función permite incluir las rutas de una aplicación en las rutas del proyecto.
- La función `RedirectView` se importa desde el módulo `django.views.generic.base`. Esta función permite redireccionar una ruta a otra ruta.
- La ruta `admin/` se asocia a la aplicación de administración de Django.
- La ruta `facts/` se asocia a la aplicación creada.
- La ruta raíz del sitio se redirecciona a la ruta `facts/`.

Con lo anterior, ya tenemos la aplicación creada y configurada. Ahora debemos ejecutar el servidor para probarla. Para ello, ejecutaremos el siguiente comando:

```bash
python manage.py runserver
```

Por defecto, Django ejecuta el servidor en el puerto 8000. Por lo tanto, podemos acceder a la aplicación desde la siguiente URL: [http://127.0.0.1:8000](http://127.0.0.1:8000).
