# Unidad 3: Django y MySQL

Construye API RESTFul usando como autenticación JWT, según requerimiento.

## Paso a paso

En la unidad anterior, agregamos la autenticación a nuestro proyecto Django. El proyecto resultante quedó con la siguiente estructura:

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
│ │ ├── 0002_initial_data.py
│ │ └── 0003_fact_user.py
│ ├── templates/
│ │ └── facts/
│ │   ├── base.html
│ │   ├── create_fact.html
│ │   ├── home.html
│ │   ├── login.html
│ │   └── register.html
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

Ahora, vamos a agregar la funcionalidad de API RESTFul a nuestro proyecto. Para ello, vamos a instalar las siguientes dependencias:

```bash
pip install djangorestframework django-cors-headers mysqlclient
```

Luego, vamos a agregar o modificar las siguientes líneas en nuestro archivo `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chuck_norris_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

CORS_ORIGIN_ALLOW_ALL = True
```

> **Nota:** Recuerda que debes cambiar los datos de conexión a MySQL por los que estés usando en tu entorno.

Ahora, vamos a crear la base de datos en MySQL. Para ello, vamos a ejecutar los siguientes comandos:

- Nos conectamos a MySQL:

  ```bash
  mysql -u root -p
  ```

- Creamos la base de datos:

  ```sql
  CREATE DATABASE chuck_norris_db;
  ```

- Salimos de MySQL:

  ```sql
  exit;
  ```

Ahora estamos listos para crear las tablas de nuestra base de datos. Para ello, vamos a ejecutar el siguiente comando:

```bash
python manage.py migrate
```

> **Nota:** Recuerda crear un superusuario, si es que no has creado uno, antes ed realizar la migración, usando el comando `python manage.py createsuperuser`.

En seguida, vamos a crear una aplicación llamada `api` que será la encargada de manejar la lógica de nuestra API RESTFul. Para ello, vamos a ejecutar el siguiente comando:

```bash
python manage.py startapp api
```

Ahora, vamos a agregar la aplicación `api` a nuestro archivo `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'api',
]
```

Con la aplicación creada, vamos a crear un archivo llamado `serializers.py` en la carpeta `api` con el siguiente contenido:

```python
from facts.models import Fact
from rest_framework import serializers

class FactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fact
        fields = '__all__'
```

Luego, vamos a modificar el archivo llamado `views.py` en la carpeta `api` con el siguiente contenido:

```python
from django.http import Http404
from facts.models import Fact
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FactSerializer

class FactList(APIView):
    def get(self, request):
        facts = Fact.objects.all()
        serializer = FactSerializer(facts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FactDetail(APIView):
    def get_fact(self, id):
        try:
            return Fact.objects.get(id=id)
        except Fact.DoesNotExist:
            raise Http404

    def get(self, request, id):
        fact = self.get_fact(id)
        serializer = FactSerializer(fact)
        return Response(serializer.data)

    def put(self, request, id):
        fact = self.get_fact(id)
        serializer = FactSerializer(fact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        fact = self.get_fact(id)
        fact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

El código anterior nos dará la capacidad de crear las vistas necesarias para nuestra API RESTFul. La clase `FactList` nos ofrecerá las opciones de listar y crear hechos. Por su parte, la clase `FactDetail` nos proporcionará los métodos para obtener, editar y eliminar un hecho específico. Cabe destacar el método `get_fact` que nos permitirá obtener un hecho específico mediante su ID o lanzar un error 404 si no existe.

Luego, vamos a crear un archivo llamado `urls.py` en la carpeta `api` con el siguiente contenido:

```python
from django.urls import path

from .views import FactList, FactDetail

urlpatterns = [
    path('facts/', FactList.as_view()),
    path('facts/<int:id>/', FactDetail.as_view()),
]
```

Es necesario entender que los patrones de URL deben ser únicos y específicos según el recurso que se quiera acceder. En este caso, la ruta `facts/` nos permitirá acceder a la lista de hechos, mientras que la ruta `facts/<int:id>/` nos permitirá acceder a un hecho específico. De esta forma, no es necesario especificar diferentes URLs para cada acción, sino que se puede usar una sola URL y especificar el método HTTP que se quiere usar. Por ejemplo, la ruta `facts/<int:id>/` nos permitirá obtener un hecho específico con el método `GET`, editarlo con el método `PUT` y eliminarlo con el método `DELETE`.

Ahora, vamos a modificar el archivo llamado `urls.py` en la carpeta `chuck_norris` con el siguiente contenido:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    ...
    path('api/', include('api.urls')),
]
```

Para probar nuestra API RESTFul, vamos a ejecutar el siguiente comando:

```bash
python manage.py runserver
```

Luego, vamos a utilizar una herramienta como Postman o cURL, y vamos a acceder a la ruta `http://127.0.0.1:8000/api/facts/`.

Veamos un ejemplo con cURL:

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/facts/' \
--header 'Content-Type: application/json'
```

Podremos ver una respuesta como la siguiente:

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
  {
    "id": 3,
    "fact": "Chuck Norris es la medida del sistema internacional del dolor.",
    "created_at": "2023-07-10T10:24:33.093671-04:00",
    "updated_at": "2023-07-10T10:24:33.093698-04:00",
    "user": 1
  },
  {
    "id": 4,
    "fact": "Chuck Norris ganó un concurso sobre permanecer debajo del agua y ganó. Cabe destacar que su contrincante era pez.",
    "created_at": "2023-07-10T10:24:33.095716-04:00",
    "updated_at": "2023-07-10T10:24:33.095744-04:00",
    "user": 1
  },
  {
    "id": 5,
    "fact": "Las lágrimas de Chuck Norris curan el cáncer. Lástima que jamás haya llorado.",
    "created_at": "2023-07-10T10:24:33.097582-04:00",
    "updated_at": "2023-07-10T10:24:33.097610-04:00",
    "user": 1
  },
  {
    "id": 6,
    "fact": "Chuck Norris dona sangre a menudo. Pero rara vez es la suya.",
    "created_at": "2023-07-10T10:24:33.099355-04:00",
    "updated_at": "2023-07-10T10:24:33.099379-04:00",
    "user": 1
  },
  {
    "id": 7,
    "fact": "La gente usa pijamas de Superman. Superman usa pijamas de Chuck Norris.",
    "created_at": "2023-07-10T10:24:33.101428-04:00",
    "updated_at": "2023-07-10T10:24:33.101457-04:00",
    "user": 1
  }
]
```

Para probar las otras funcionalidades, podemos utilizar las siguientes rutas:

- POST `http://127.0.0.1:8000/api/facts/`: Nos permitirá crear un nuevo hecho.

  ```bash
  curl --location --request POST 'http://127.0.0.1:8000/api/facts/' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "fact": "Chuck Norris puede escribir aplicaciones multihilo con un solo hilo."
  }'
  ```

  ```json
  {
    "id": 8,
    "fact": "Chuck Norris puede escribir aplicaciones multihilo con un solo hilo.",
    "created_at": "2023-07-10T10:24:33.103567-04:00",
    "updated_at": "2023-07-10T10:24:33.103593-04:00",
    "user": 1
  }
  ```

- GET `http://127.0.0.1:8000/api/facts/8/`: Nos retornará un hecho específico. En este caso, el hecho con el ID 8.

  ```bash
  curl --location --request GET 'http://127.0.0.1:8000/api/facts/8/' \
  --header 'Content-Type: application/json'
  ```

  ```json
  {
    "id": 8,
    "fact": "Chuck Norris puede escribir aplicaciones multihilo con un solo hilo.",
    "created_at": "2023-07-10T10:24:33.103567-04:00",
    "updated_at": "2023-07-10T10:24:33.103593-04:00",
    "user": 1
  }
  ```

- PUT `http://127.0.0.1:8000/api/facts/8/`: Nos permitirá editar un hecho específico. En este caso, el hecho con el ID 8.

  ```bash
  curl --location --request PUT 'http://127.0.0.1:8000/api/facts/8/' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "fact": "Chuck Norris no necesita un depurador, se limita a mirar fijamente al fallo hasta que el código confiesa."
  }'
  ```

  ```json
  {
    "id": 8,
    "fact": "Chuck Norris no necesita un depurador, se limita a mirar fijamente al fallo hasta que el código confiesa.",
    "created_at": "2023-07-10T10:24:33.103567-04:00",
    "updated_at": "2023-07-10T10:24:33.103593-04:00",
    "user": 1
  }
  ```

- DELETE `http://127.0.0.1:8000/api/facts/8/`: Nos permitirá eliminar un hecho específico. En este caso, el hecho con el ID 8.

  ```bash
  curl --location --request DELETE 'http://127.0.0.1:8000/api/facts/8/'
  ```

Ahora es momento de añadir la funcionalidad de seguridad a nuestra API RESTFul. Para ello, vamos a modificar el archivo `settings.py` en la carpeta `chuck_norris` con el siguiente contenido:

```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
]
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
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FactSerializer

class FactList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    ...

    def post(self, request):
        serializer = FactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) # Agregamos el usuario autenticado al serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FactDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    ...
```

De esta forma, solo aquellas vistas que requieran autenticación podrán ser accedidas por usuarios autenticados, mientras que aquellas que no dispongan de esta configuración podrán ser accedidas por cualquier usuario.

Si necesitamos que todas las vistas de nuestra API RESTFul requieran autenticación, podemos modificar el archivo llamado `settings.py` en la carpeta `chuck_norris` con el siguiente contenido:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

> **Nota:** Recuerda que este paso es solo cuando quieres hacer que todas las vistas requieran autenticación.

Este cambio nos permitirá eliminar las líneas de código que añadimos anteriormente en el archivo llamado `views.py` en la carpeta `api`, y establecerá por defecto que todas las vistas requieran autenticación.

Ahora, vamos a crear la ruta para obtener el token de autenticación. Para ello, vamos a modificar el archivo llamado `urls.py` en la carpeta `api` con el siguiente contenido:

```python
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import FactList, FactDetail

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('facts/', FactList.as_view()),
    path('facts/<int:id>/', FactDetail.as_view()),
]
```

Para probar nuestra API RESTFul, vamos a ejecutar el siguiente comando:

```bash
python manage.py runserver
```

Si accedemos a la url `http://127.0.0.1:8000/api/facts/` en el navegador, obtendremos una respuesta similar a esta:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

La razón es que necesitamos autenticarnos para poder acceder a la API RESTFul, y como no lo hemos hecho, nos devuelve un error `401 Unauthorized`.

Para poder acceder a las rutas protegidas, usando una herramienta como Postman o cURL, vamos a realizar una petición POST a la URL `http://127.0.0.1:8000/api/auth/` con el siguiente contenido:

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
  "token": "c61ed8ee590fe4fb03a8bc7a5abff0bf7c9bcbfc"
}
```

> **Nota:** El valor del token que obtengas será diferente al que se muestra en este ejemplo.

Ahora, vamos a realizar una petición GET a la URL `http://127.0.0.1:8000/api/facts/`. Si usamos una herramienta como Postman, debemos modificar la autorización de la petición para que use el token que obtuvimos anteriormente. Si usamos cURL, debemos añadir el token en el header de la petición de la siguiente forma:

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/facts/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token c61ed8ee590fe4fb03a8bc7a5abff0bf7c9bcbfc'
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

Para incorporar la información del usuario en las respuestas de la API RESTFul, vamos a modificar el archivo llamado `serializers.py` en la carpeta `api` con el siguiente contenido:

```python
from django.contrib.auth.models import User
from facts.models import Fact
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff',
                   'is_active', 'date_joined', 'groups', 'user_permissions')

class FactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Fact
        fields = '__all__'
        depth = 1
```

De esta forma, al consultar la url `http://127.0.0.1:8000/api/facts/` obtendremos una respuesta similar a esta:

```json
[
  {
    "id": 1,
    "fact": "Chuck Norris puede dividir entre cero.",
    "created_at": "2023-07-10T10:24:33.088738-04:00",
    "updated_at": "2023-07-10T10:24:33.088764-04:00",
    "user": {
      "id": 1,
      "username": "admin",
      "first_name": "",
      "last_name": "",
      "email": "admin@example.com"
    }
  },
  {
    "id": 2,
    "fact": "Hay 1424 cosas en una habitación promedio con las que Chuck Norris podría matarte. Incluyendo la habitación en sí.",
    "created_at": "2023-07-10T10:24:33.091441-04:00",
    "updated_at": "2023-07-10T10:24:33.091476-04:00",
    "user": {
      "id": 1,
      "username": "admin",
      "first_name": "",
      "last_name": "",
      "email": "admin@example.com"
    }
  },
  ...
]
```

Por último, eliminamos el archivo `db.sqlite3` y nuestra aplicación estará lista.
