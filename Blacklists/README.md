# Servicio de Blacklists

## Descripción general

Esta sección describe los servicios desarrollados en Python 3.10 utilizando Flask como framework web y PostgreSQL como base de datos.

## Instalación
### Prerrequisitos

- Python 3.9 o 3.10
- Docker
- Docker Compose
- Postgres
- Postman
- Clonar el repositorio

### Configuración del entorno (Opción 1)

En la raíz del proyecto de Balcklists `./Blacklists`, debe existir un archivo ```.env``` con la siguiente configuración:
```
DB_USER: Usuario de la base de datos
DB_PASSWORD: Contraseña de la base de datos
DB_HOST: Host de la base de datos
DB_PORT: Puerto de la base de datos (default: 5432)
DB_NAME: Nombre de la base de datos
USERS_PATH: URI Base del servicio de usuarios
```

1. Crear un entorno virtual:

```
python -m venv venv
```
2. Activar el entorno virtual:

```
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```
3. Instalar dependencias:

```
pip install -r requirements.txt
```

4. Ejecutar la aplicación:
```
flask run --host=0.0.0.0 --port=3000
```

### Uso de Docker Compose (Opción 2)

#### Levantar solo el servicio de Balcklists

1. Levantar solo el servicio de Balcklists desde un directorio atrás, mismo nivel de Balcklists, se puede ejecutar el siguiente comando para levantar solo los servicios relacionados con Balcklists:
   Para levantar únicamente el servicio relacionado con las Balcklists, incluyendo la base de datos de Balcklists y el propio servicio de Balcklists, puedes ejecutar el siguiente comando:

```
docker-compose up -d blacklist_db blacklist blacklist_net
```

Esto iniciará los siguientes servicios:
- blacklist_db: Base de datos PostgreSQL para el servicio de Balcklists.
- blacklist: Servicio de Balcklists que se conectará a blacklist_db.
- blacklist_net: Red de Docker utilizada por estos servicios.

## Descripción de los Endpoints

### 1. Crear una cuenta en la blacklist

**URL:** `/blacklists`  
**Método:** `POST`  
**Descripción:** Crea una nueva cuenta en la blacklist. Solo los usuarios autenticados pueden crear una blacklist.  
**Datos de entrada (JSON):**
```json
{
    "email": "correo eletrónico de la cuenta",
    "app_uuid": "uuid de la apicación",
    "blocked_reason": "razón por la que fue agregado a la blacklist"
}
```
- Cuando una solicitud POST se procesa correctamente, el servidor devuelve un código de estado 201 Created y un mensaje de :
Datos de salida (JSON):
```json
{
    "id": "817ddd38-8876-4496-bbeb-9003bfc3e4e5",
    "msg": "Cuenta creada correctamente"
}
```
- Nota Importante
Los errores de autorización (401, 403) y los errores relacionados con los campos (400, 412) no incluyen un mensaje detallado en el cuerpo de la respuesta, solo el código de error.

  Los errores de autorización (401, 403) y los errores relacionados con los campos (400, 412) no incluyen un mensaje detallado en el cuerpo de la respuesta, solo el código de error.

### 2. Consultar detalles de una blacklist
**URL:** `/blacklists/<email>`  
**Método:** `GET`  
**Descripción:** Consulta si la cuenta existe dentro de una blacklist.   

Datos de salida (JSON):
```json
{
    "existe": true,
    "blocked_reason": "narco"
}
```
- Nota Importante
  Los errores de autorización (401, 403) y los errores relacionados con los campos (400, 412) no incluyen un mensaje detallado en el cuerpo de la respuesta, solo el código de error.


### 3. Verificar el estado del servicio
**URL:** `/blacklists/ping`  
**Método:** `GET`  
**Descripción:** Verifica si el servicio de Balcklists está activo.   

Respuesta exitosa (200):
```
"pong"
```

### 4. Limpiar la base de datos
**URL:** `/blacklists/reset`  
**Método:** `POST`  
**Descripción:** Limpia todas las Balcklists en la base de datos.

Respuesta exitosa (200):
```json
{
  "msg": "Todos los datos fueron eliminados"
}
```






