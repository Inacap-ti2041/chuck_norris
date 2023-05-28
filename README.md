# Chuck Norris Facts

Aplicación de ejemplo de programación back end con Django y MySQL.

## Tabla de contenidos

- [Introducción](#introducción)
- [Prerequisitos](#prerequisitos)
  - [Python](#python)
    - [Instalar Python en Windows](#instalar-python-en-windows)
    - [Instalar Python en macOS](#instalar-python-en-macos)
    - [Instalar Python en Linux](#instalar-python-en-linux)
  - [MySQL](#mysql)
    - [Instalar MySQL en Windows](#instalar-mysql-en-windows)
    - [Instalar MySQL en macOS](#instalar-mysql-en-macos)
    - [Instalar MySQL en Linux](#instalar-mysql-en-linux)
- [Instalación](#instalación)
- [Unidades](#unidades)
- [Licencia](#licencia)

## Introducción

Este es un proyecto educativo que utiliza Python y Django para enseñar a los alumnos sobre el desarrollo de aplicaciones web.

## Prerequisitos

### Python

#### Instalar Python en Windows

#### Instalar Python en macOS

Para instalar Python y pip en macOS, sigue estos pasos:

1. Visita el sitio web oficial de Python en <https://www.python.org/downloads/release/> y descarga el instalador de Python para macOS.
2. Ejecuta el instalador descargado y sigue las instrucciones del asistente de instalación. Asegúrate de marcar la casilla "Install pip" durante el proceso.
3. Una vez completada la instalación, abre la Terminal en tu macOS desde la carpeta "Utilidades" dentro de la carpeta "Aplicaciones".
4. Para verificar la instalación de Python, ejecuta el siguiente comando:

   ```bash
   python3 --version
   ```

   Si el comando no funciona, intenta simplemente ejecutando `python --version`. Esto mostrará la versión instalada de Python (debe ser 3.11.3).

5. Si el comando `pip3 --version` no funciona, intenta utilizar `pip --version`. Esto mostrará la versión instalada de pip.

6. Si ninguno de los comandos anteriores funciona, es posible que necesites agregar las rutas de Python y pip al archivo de configuración de tu terminal. Puedes hacerlo agregando las siguientes líneas al archivo `.bash_profile` o `.zshrc`, según el shell que utilices:

   ```bash
   export PATH="/Library/Frameworks/Python.framework/Versions/3.11/bin:$PATH"
   ```

   Guarda el archivo y reinicia la Terminal.

#### Instalar Python en Linux

Para instalar Python y pip en macOS, sigue estos pasos:

**Ubuntu/Debian:**

> **Nota:** Es importante tener en cuenta que Ubuntu ya tiene una versión de Python preinstalada.

1. Actualiza los paquetes del sistema ejecutando el siguiente comando:

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Instala Python y pip ejecutando el siguiente comando:

   ```bash
   sudo apt install python3 python3-pip
   ```

3. Verifica la instalación ejecutando el siguiente comando:

   ```bash
   python3 --version
   ```

   Si la verificación de la instalación no funciona, puedes actualizar el PATH siguiendo los siguientes pasos:

   - Detarmina la ruta de instalación de Python:

     ```bash
     which python3
     ```

   - Agrega la ruta de instalación de Python al archivo `.bashrc`:

     ```bash
     echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
     source ~/.bashrc
     ```

**RedHat/CentOS:**

1. Actualiza las dependencias del sistema ejecutando el siguiente comando:

   ```bash
   sudo yum update -y
   ```

2. Instala Python ejecutando el siguiente comando:

   ```bash
   sudo yum install -y python3
   ```

3. Verifica la instalación ejecutando el siguiente comando:

   ```bash
   python3 --version
   ```

   Si la verificación de la instalación no funciona, puedes actualizar el PATH ejecutando los siguientes comandos:

   ```bash
   echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

### MySQL

Antes de ejecutar el proyecto, se debe instalar la base de datos [MySQL](https://www.mysql.com/). Para ello, debe seguir las instrucciones específicas para cada sistema operativo.

#### Instalar MySQL en Windows

Para instalar MySQL se deben seguir las [instrucciones oficiales](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install-windows-quick.html) del proveedor.

#### Instalar MySQL en macOS

Instalar el servidor y el cliente de MySQL:

```bash
brew install mysql
```

Si no desea instalar el servidor MySQL, puede utilizar mysql-client en su lugar:

```bash
brew install mysql-client
echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.bash_profile
export PATH="/usr/local/opt/mysql-client/bin:$PATH"
```

#### Instalar MySQL en Linux

Es posible que tenga que instalar las cabeceras y bibliotecas de desarrollo de Python 3 y MySQL de la siguiente manera:

- Ubuntu/Debian

  Primero, se debe actualizar el sistema operativo:

  ```bash
  sudo apt update && sudo apt upgrade
  ```

  Luego, debemos instalar el servidor MySQL. Este proceso instala el servidor y el cliente:

  ```bash
  sudo apt install mysql-server
  ```

  Si solo se desea instalar el cliente para conectarse a una instancia remota de MySQL, se debe ejecutar este comando en lugar del anterior:

  ```bash
  sudo apt install mysql-client
  ```

  Por último, se realiza la instalación de las herramientas de desarrollo

  ```bash
  sudo apt install python3-dev default-libmysqlclient-dev build-essential
  ```

- Red Hat/CentOS

  Necesitarás actualizar el sistema escribiendo el siguiente comando:

  ```bash
  sudo yum update
  ```

  Una vez actualizado el sistema, es hora de instalar MySQL.

  ```bash
  sudo yum install mysql
  ```

  Por último, se realiza la instalación de las herramientas de desarrollo

  ```bash
  sudo yum install python3-devel mysql-devel
  ```

## Instalación

Para instalar el proyecto, se debe clonar el repositorio y luego instalar las dependencias:

```bash
git clone https://github.com/Inacap-ti2041/chuck_norris.git
cd chuck_norris
pip install -r requirements.txt
```

## Unidades

- [Unidad 1: Tecnologías del lado del servidor](./unidad_1/README.md)
- Unidad 2: Framework Backend
  - [Parte 1](./unidad_2a/README.md)
  - [Parte 2](./unidad_2b/README.md)
- [Unidad 3: Django y MySQL](./unidad_3/README.md)

## Licencia

[MIT](./LICENSE)
