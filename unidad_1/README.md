# Unidad 1: Tecnologías del lado del servidor

Realiza programa del lado del servidor, de acuerdo a la sintaxis del lenguaje.

## Paso a paso

En primer lugar, crear la carpeta donde alojaremos el proyecto. Para ello, ejecutaremos el siguiente comando:

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

> **Nota:** Es importante destacar el punto al final del comando. Ese parámetro le indica a Django que debe crear el projecto en el primer nivel del directorio.

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
import random

from django.shortcuts import HttpResponse

# Lista de hechos de Chuck Norris
FACTS_LIST = [
    "Hay 1424 cosas en una habitación promedio con las que Chuck Norris podría matarte. Incluyendo la habitación en sí.",
    "Chuck Norris es la medida del sistema internacional del dolor.",
    "Chuck Norris ganó un concurso sobre permanecer debajo del agua y ganó. Cabe destacar que su contrincante era pez.",
    "Las lágrimas de Chuck Norris curan el cáncer. Lástima que jamás haya llorado.",
    "Chuck Norris dona sangre a menudo. Pero rara vez es la suya.",
    "La gente usa pijamas de Superman. Superman usa pijamas de Chuck Norris."
]


def home(request):
    # Seleccionamos un hecho aleatorio
    current_fact = random.choice(FACTS_LIST)
    # Creamos el contenido de la respuesta
    content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chuck Norris</title>
    </head>
    <body>
        <p>Este es un hecho de Chuck Norris</p>
        <blockquote>{current_fact}</blockquote>
    </body>
    </html>
    """
    # Creamos la respuesta
    return HttpResponse(content)
```

La función llamada `home` es la encargada de generar la respuesta. En este caso, se genera un hecho aleatorio de Chuck Norris. Para lograrlo, se utiliza la función `random.choices` que recibe como parámetro una lista de elementos y retorna un elemento aleatorio de la lista. Luego, se crea el contenido de la respuesta, el cual es un documento HTML. Finalmente, se retorna la respuesta con el contenido creado.

Ahora debemos crear el archivo `urls.py` en la carpeta `facts`. Este archivo es el encargado de definir las rutas de la aplicación.

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

En el archivo anterior, se importa la función `path` desde el módulo `django.urls`. Luego, se importa el módulo `views` de la aplicación. Finalmente, se define la ruta de la aplicación, la cual es la raíz del sitio. Esta ruta se asocia a la función `home` de la aplicación.

Con las rutas definidas, debemos modificar el archivo `urls.py` de la carpeta `chuck_norris`.

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('facts.urls')),
]
```

En el archivo anterior, se importa la función `include` desde el módulo `django.urls`. Luego, se define la ruta de la aplicación, la cual es la raíz del sitio. Esta ruta se asocia a la función `home` de la aplicación.

Con lo anterior, ya tenemos la aplicación creada y configurada. Ahora debemos ejecutar el servidor para probarla. Para ello, ejecutaremos el siguiente comando:

```bash
python manage.py runserver
```

Por defecto, Django ejecuta el servidor en el puerto 8000. Por lo tanto, podemos acceder a la aplicación desde la siguiente URL: [http://localhost:8000](http://localhost:8000).
