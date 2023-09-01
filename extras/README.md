# Extras

En este apartado se encuentran algunos elementos adicionales, útiles al momento de programar aplicaciones web o APIs RESTFul con Django.

## Tabla de contenidos

- [Entorno Virtual](#entorno-virtual)
- [Archivo `requirements.txt`](#archivo-requirementstxt)
- [Variables de Entorno](#variables-de-entorno)
- [Autenticación con JWT](#autenticación-con-jwt)

## Entorno Virtual

Un entorno virtual es un espacio aislado en el que se pueden instalar paquetes de Python sin afectar al resto del sistema. Esto permite tener diferentes versiones de paquetes en cada proyecto, sin que se produzcan conflictos entre ellos.

Para crear un entorno virtual, necestamos instalar el paquete `virtualenv` de Python. Para ello, ejecutamos el siguiente comando:

```bash
# Se actualiza pip a la última versión
python -m pip install --upgrade pip
# Se instala virtualenv
pip install virtualenv
```

Una vez instalado el paquete, podemos crear un entorno virtual ejecutando el siguiente comando:

```bash
virtualenv <nombre_entorno>
```

Si estás trabajando en Windows y recibes el siguiente mensaje de error al ejecutar el comando anterior:

```cmd
"virtualenv" no se reconoce como un comando interno o externo,
programa o archivo por lotes ejecutable.
```

O bien, si recibe el siguiente mensaje de error:

```ps1
virtualenv: The term 'virtualenv' is not recognized as a name of a cmdlet, function, script file, or executable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
```

Entonces debe ejecutar el comando:

```cmd
python -m virtualenv <nombre_entorno>
```

> **Nota:** Recuerda reemplazar `<nombre_entorno>` por el nombre que desees darle al entorno virtual. Los más comunes son `venv` y `env`, aunque puedes utilizar el nombre que desees. Solo asegúrate de no utilizar espacios en blanco ni caracteres especiales.

Para activar el entorno virtual, debes estar en el directorio del proyecto. El comando para activar el entorno virtual varía según el sistema operativo:

- **Windows:**

  ```cmd
  <nombre_entorno>\Scripts\activate
  ```

- **Linux / macOS:**

  ```bash
  source <nombre_entorno>/bin/activate
  ```

Una vez activado el entorno virtual, el nombre del entorno virtual aparecerá entre paréntesis en la consola:

- **Windows:**

  ```cmd
  (<nombre_entorno>) C:\Users\Usuario\Proyectos\proyecto>
  ```

- **Linux / macOS:**

  ```bash
  (<nombre_entorno>) usuario@proyecto:~$
  ```

Para desactivar el entorno virtual, ejecutamos el siguiente comando:

```bash
deactivate
```

## Archivo `requirements.txt`

El archivo `requirements.txt` es un archivo de texto plano que contiene una lista de paquetes de Python que se deben instalar para ejecutar el proyecto. Es muy útil para compartir el proyecto con otros desarrolladores, ya que permite instalar todas las dependencias del proyecto con un solo comando.

Este archivo se puede generar automáticamente con el comando `pip freeze`:

```bash
pip freeze > requirements.txt
```

> **Nota:** Recuerda que debes estar en el directorio del proyecto para ejecutar este comando, y que si vas a generar el archivo `requirements.txt` en un entorno virtual, debes activarlo primero.

Para instalar los paquetes listados en el archivo `requirements.txt`, ejecutamos el siguiente comando:

```bash
pip install -r requirements.txt
```

> **Nota:** Recuerda que debes estar en el directorio del proyecto para ejecutar este comando, y que si vas a instalar los paquetes en un entorno virtual, debes activarlo primero.

## Variables de Entorno

Las variables de entorno son variables globales que se pueden utilizar en el sistema operativo. Estas variables se pueden utilizar para almacenar información sensible, como contraseñas, claves de acceso, tokens, etc. Esto permite que la información sensible no se almacene en el código fuente, sino en el sistema operativo, permitiendo que estos valores cambien sin necesidad de modificar el código fuente. También es muy útil para compartir el código fuente con otros desarrolladores, ya que permite que cada desarrollador utilice sus propios valores para las variables de entorno.

Python cuenta con la librearía `os` para trabajar con variables de entorno. Para utilizarla, debemos importarla en el archivo `settings.py`:

```python
import os
```

Para acceder a una variable de entorno, utilizamos el método `get()` de la librería `os`:

```python
SECRET_KEY = os.environ.get('SECRET_KEY')
```

Para definir una variable de entorno, debemos utilizar el comando `export` en Linux o macOS, o el comando `set` en Windows:

- **Windows:**

  ```cmd
  set SECRET_KEY=valor_secreto
  ```

- **Linux / macOS:**

  ```bash
  export SECRET_KEY=valor_secreto
  ```

> **Nota:** Recuerda que debes estar en el directorio del proyecto para ejecutar estos comandos, y que si vas a definir las variables de entorno en un entorno virtual, debes activarlo primero.

Pero hay veces en las que necesitamos que las variables de entorno sean diferentes en cada entorno. Por ejemplo, en el entorno de desarrollo podemos utilizar una base de datos SQLite, mientras que en el entorno de producción podemos utilizar una base de datos PostgreSQL. Para ello, podemos utilizar el paquete `django-environ`, que nos permite definir variables de entorno en un archivo `.env` y cargarlas en el sistema operativo.

Para instalar el paquete `django-environ`, ejecutamos el siguiente comando:

```bash
pip install django-environ
```

Una vez instalado el paquete, debemos importarlo en el archivo `settings.py`:

```python
import environ
```

Para cargar las variables de entorno, debemos crear una instancia de la clase `Env` del paquete `django-environ`:

```python
env = environ.Env()
```

Para cargar las variables de entorno del archivo `.env`, utilizamos el método `read_env()` de la instancia de la clase `Env`:

```python
# Leer variables de entorno del archivo .env
environ.Env.read_env(env_file='path/to/.env')
# O
env.read_env(env_file='path/to/.env')
```

> **Nota:** El parámetro `env_file` es opcional. Si no se especifica, el paquete buscará un archivo `.env` en el directorio del proyecto. Aunque los desarrolladores del paquete recomiendan especificar el parámetro `env_file` para evitar problemas de seguridad.

Para acceder a una variable de entorno, utilizamos el método `get()` de la instancia de la clase `Env`:

```python
SECRET_KEY = env.get('SECRET_KEY')
```

Para definir una variable de entorno, debemos crear un archivo `.env` en el directorio del proyecto y definir las variables de entorno en el siguiente formato:

```env
SECRET_KEY=valor_secreto
```

> **Nota:** Recuerda que debes estar en el directorio del proyecto para crear el archivo `.env`, y que si vas a instalar el paquete en un entorno virtual, debes activarlo primero.

Un ejemplo de archivo `settings.py` utilizando el paquete `django-environ`:

```python
import os
from pathlib import Path

import environ

# Initialise environment variables
env = environ.Env(DEBUG=(bool, False))

# Set the project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Read the .env file
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

# Set the DEBUG, SECRET_KEY and ALLOWED_HOSTS environment variables
DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env.str('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
...
DATABASES = {
    'default': env.db()
}
```

En el código anterior, podemos observar que algunas instrucciones incluyen un valor por defecto, como es el caso de `env.bool('DEBUG', default=False)`. Esto implica que, si la variable de entorno no se encuentra definida, se utilizará el valor por defecto. En el caso de no contar con un valor por defecto, como la instrucción `env.str('SECRET_KEY')`, es obligatorio que la variable de entorno se encuentre definida, ya sea en el sistema operativo o en el archivo `.env`. De lo contrario, se lanzará una excepción.

> **Nota:** Las variables de entorno definidas en el archivo `.env` tienen prioridad sobre las definidas en el sistema operativo. Por ejemplo, si definimos la variable de entorno `DEBUG` en el sistema operativo con el valor `False`, pero en el archivo `.env` la definimos con el valor `True`, el valor que se utilizará será el del archivo `.env`.

La sección de bases de datos, usa la instrucción `env.db()` para definir la configuración de la base de datos. Esta instrucción utiliza la variable de entorno `DATABASE_URL` para obtener la configuración de la base de datos. Esta variable de entorno debe tener el siguiente formato: `engine://user:password@host:port/dbname`, donde `engine` es el motor de base de datos, `user` es el usuario de la base de datos, `password` es la contraseña del usuario, `host` es el host de la base de datos, `port` es el puerto de la base de datos y `dbname` es el nombre de la base de datos. Esos valores deben ser reemplazados por los valores reales de la base de datos que estemos utilizando.

Django incorpora los siguientes controladores de base de datos:

| Base de datos | Controlador                     |
| ------------- | ------------------------------- |
| PostgreSQL    | `django.db.backends.postgresql` |
| MySQL         | `django.db.backends.mysql`      |
| SQLite        | `django.db.backends.sqlite3`    |
| Oracle        | `django.db.backends.oracle`     |

También puedes usar un backend de base de datos que no venga con Django estableciendo ENGINE a una ruta completamente cualificada. Por ejemplo, `mypackage.backends.whatever`. Siguiendo con el ejemplo anterior, si queremos utilizar el controlador de base de datos de MSSQL, debemos instalar el paquete `sql_server.pyodbc`, y luego usar el constructor correspondiente.

Algunos ejemplos de valores para la variable de entorno `DATABASE_URL`:

| Base de datos | URL                                                    |
| ------------- | ------------------------------------------------------ |
| MySQL         | `mysql://root:root@localhost:3306/dbname`              |
| PostgreSQL    | `postgresql://postgres:postgres@localhost:5432/dbname` |
| SQLite        | `sqlite:///db.sqlite3`                                 |
| Oracle        | `oracle://user:password@localhost:1521/dbname`         |
| MSSQL         | `mssql://user:password@localhost:1433/dbname`          |

Ahora, volviendo al ejemplo, para ejecutar nuestro proyecto incluyendo las variables de entorno, vamos a crear un archivo `.env` en el directorio del proyecto, al mismo nivel del archivo `manage.py`, y definir las variables de entorno en el siguiente formato:

```env
DEBUG=True
SECRET_KEY=cYE?7LnGqB9$h?&@s&XFDze@z6&5xAe?SF3nhjM!
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=mysql://root:password@localhost:3306/chuck_norris_db
```

> **Nota:** Es importante tener en cuenta que el archivo `.env` no debe ser compartido con otros desarrolladores, ya que contiene información sensible.

En la carpeta del proyecto, vas a encontrar un archivo llamado [`.env.example`](.env.example) con un ejemplo que puedes utilizar como base para crear tu archivo `.env`. Ahí puedes reemplazar los valores por defecto por los valores que correspondan a tu proyecto.

## Autenticación con JWT

JWT (JSON Web Token) es un estándar abierto basado en JSON propuesto por IETF (RFC 7519) para la creación de tokens de acceso que permiten la propagación de identidad y privilegios entre dos partes de forma segura, confiable y simple.

La ventaja de usar tokens JWT es que no necesitamos almacenarlos en la base de datos, ya que son generados usando un algoritmo de encriptación, en comparación con los tokens tradicionales que vienen con Django Rest Framework. Esto nos permite escalar nuestra aplicación sin tener que preocuparnos por el almacenamiento de los tokens.

Para incorporar la autenticación con JWT en nuestro proyecto, vamos a utilizar el paquete `djangorestframework-simplejwt`. Este paquete nos permite generar tokens JWT para autenticar a los usuarios en nuestra API. Lo primero que debemos hacer es instalar el paquete:

```bash
pip install djangorestframework-simplejwt
```

Luego, debemos modificar el archivo `settings.py` en la carpeta `chuck_norris`, con el siguiente código:

```python
import os
from datetime import timedelta
from pathlib import Path

import environ

...

INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
]

...

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
```

Como agregamos una nueva aplicación, es necesario ejecutar las migraciones para que se cree la tabla correspondiente en la base de datos:

```bash
python manage.py migrate
```

Hecho esto, vamos a modificar el archivo llamado `views.py` en la carpeta `api` con el siguiente contenido:

```python
from django.http import Http404
from facts.models import Fact
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import FactSerializer

class FactList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    ...


class FactDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    ...
```

Hay que resaltar que en ambas clases modificamos el atributo `authentication_classes` para usar el valor `JWTAuthentication`, en lugar del valor `TokenAuthentication` que usamos en la [unidad 3](../unidad_3/README.md).

De esta forma, solo aquellas vistas que requieran autenticación podrán ser accedidas por usuarios autenticados, mientras que aquellas que no dispongan de esta configuración podrán ser accedidas por cualquier usuario.

Si necesitamos que todas las vistas de nuestra API RESTFul requieran autenticación, podemos modificar el archivo llamado `settings.py` en la carpeta `chuck_norris` con el siguiente contenido:

```python
...
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    ...
}
...
```

Acá también debemos resaltar que modificamos el atributo `DEFAULT_AUTHENTICATION_CLASSES` para usar el valor `rest_framework_simplejwt.authentication.JWTAuthentication`, en lugar del valor `rest_framework.authentication.TokenAuthentication` que usamos en la [unidad 3](../unidad_3/README.md).

Luego, debemos modificar el archivo `urls.py` en la carpeta `api`, con el siguiente código:

```python
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import FactDetail, FactList

urlpatterns = [
    path('auth/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('facts/', FactList.as_view()),
    path('facts/<int:id>/', FactDetail.as_view()),
]
```

En este caso, modificamos la ruta `auth/` para que use la vista `TokenObtainPairView` y agregamos la ruta `auth/refresh/` para que use la vista `TokenRefreshView`. Esta última vista nos permitirá obtener un nuevo token de acceso, en caso de que el token de acceso que tengamos haya expirado.

Para probar nuestra API RESTFul, vamos a ejecutar el siguiente comando:

```bash
python manage.py runserver
```

Usando una herramienta como Postman o cURL, vamos a realizar una petición POST a la URL `http://127.0.0.1:8000/api/auth/` con el siguiente contenido:

```json
{
  "username": "admin",
  "password": "admin"
}
```

Veamos un ejemplo de petición con cURL:

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/auth/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "admin",
    "password": "admin"
}'
```

> Nota: Debes reemplazar el valor de `username` y `password` por los valores que hayas configurado al momento de crear el superusuario.

La petición anterior deberá retornar una respuesta similar a esta:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MDMwNTE1MiwiaWF0IjoxNjg5MDk1NTUyLCJqdGkiOiJhNzVkNzMxY2MzNjk0ZmZkOWFmNTE2YWEzOWY5M2QzOSIsInVzZXJfaWQiOjJ9._bHTHpfL3AxqxSGxitiHBrWmT4Zc5HXos0nkEWH9xzc",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5MDk2NDUyLCJpYXQiOjE2ODkwOTU1NTIsImp0aSI6Ijk1Y2Q2YThhYzQwMDQ0NTJiZGQyZGYxNWU5MTU2OGQ5IiwidXNlcl9pZCI6Mn0.q0FxumZR8LFr6W7dzLA8r2tBLQ0LRRUGpXV2fM4_4zU"
}
```

> **Nota:** El valor que obtengas será diferente al que se muestra en este ejemplo.

Ahora, vamos a realizar una petición GET a la URL `http://127.0.0.1:8000/api/facts/`. Si usamos una herramienta como Postman, debemos modificar la autorización de la petición para que use el token `access` que obtuvimos anteriormente. Si usamos cURL, debemos añadir el token en el header de la petición de la siguiente forma:

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/facts/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5MDk2NDUyLCJpYXQiOjE2ODkwOTU1NTIsImp0aSI6Ijk1Y2Q2YThhYzQwMDQ0NTJiZGQyZGYxNWU5MTU2OGQ5IiwidXNlcl9pZCI6Mn0.q0FxumZR8LFr6W7dzLA8r2tBLQ0LRRUGpXV2fM4_4zU'
```

De esta forma, vamos a poder obtener una respuesta positiva:

```json
[
  {
    "id": 1,
    "fact": "Chuck Norris puede dividir entre cero.",
    "created_at": "2023-07-10T10:24:33.088738-04:00",
    "updated_at": "2023-07-10T10:24:33.088764-04:00",
    "user": 1
  },
  {
    "id": 2,
    "fact": "Hay 1424 cosas en una habitación promedio con las que Chuck Norris podría matarte. Incluyendo la habitación en sí.",
    "created_at": "2023-07-10T10:24:33.091441-04:00",
    "updated_at": "2023-07-10T10:24:33.091476-04:00",
    "user": 1
  },
  ...
]
```

Cabe notar que la diferencia entre esta llamada y las revisadas en la [unidad 3](../unidad_3/README.md), es que reemplazamos `Token` por `Bearer` en el header de la petición.

Para mayor infomación sobre el uso de tokens JWT en Django, puedes revisar la documentación oficial de Django Rest Framework Simple JWT: [https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html)
