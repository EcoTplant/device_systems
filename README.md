# device_systems API

API REST para la administración de usuarios del sistema **device_systems**.  
Construida con **FastAPI** (Python 3.13) y **Uvicorn** como servidor ASGI.

## Descripción

La aplicación permite gestionar usuarios con las siguientes operaciones:

- Listar todos los usuarios (con soporte de filtros por `role` y `is_active`).
- Obtener un usuario específico mediante su ID.
- Registrar nuevos usuarios con validaciones (nombre mínimo 3 caracteres, email único y con formato válido, roles permitidos: `admin`, `support`, `user`).

La API incluye documentación automática interactiva (**Swagger UI** y **ReDoc**) y responde con cabeceras personalizadas (`X-App-Name`, `X-API-Version`).

## Instalación de dependencias

## Requisitos
- Python 3.13
- FastAPI 0.115.0
- Uvicorn 0.31.0

## Instalación
1. Crear entorno virtual: `python -m venv env`
2. Activar entorno: `env\Scripts\activate` (Windows) o `source env/bin/activate` (Linux/Mac)
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar: `uvicorn app.main:app --reload`

## Endpoints
| Método | Ruta                     | Descripción                          |
|--------|--------------------------|--------------------------------------|
| GET    | /users                   | Listar usuarios (filtro por role/is_active) |
| GET    | /users/{user_id}         | Obtener usuario por ID               |
| POST   | /users                   | Crear nuevo usuario                  |

## Documentación interactiva
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

###  Ejemplos de peticiones

## Listar todos los usuarios

![Petición GET sin filtros](images/getsinfiltros.png)

## GET con filtro por rol:

![Petición GET con filtros](images/getfiltrorol.png)

## Obtener usuario por ID

# Respuesta exitosa 

![Petición GET con filtros](images/getfiltroid200.png)

## Crear nuevo usuario

# Respuesta exitosa

![Petición POST - Nuevo usuario](images/post201.png)

# Respuesta por email duplicado

![Petición POST - Nuevo usuario](images/post400.png)

# Respuesta por validación fallida

![Petición POST - Nuevo usuario](images/post422.png)

##  Capturas de Swagger UI

![Swagger UI](images/swaggerui.png)

## Tecnologías utilizadas

- Python 3.13
- FastAPI 0.115.0
- Uvicorn 0.31.0 (con dependencias estándar)
- Pydantic (para validaciones y modelos)


```markdown
# device_systems API

API REST completa para la gestión de usuarios del sistema **device_systems**.  
Permite operaciones CRUD (Crear, Leer, Actualizar, Eliminar) con validaciones, filtros, manejo de errores y documentación interactiva automática.

## 📖 Descripción

La API expone un recurso `/users` sobre el cual se pueden realizar las siguientes operaciones:

- Listar todos los usuarios (con soporte de filtros por `role` y `is_active`).
- Obtener un usuario específico por su ID.
- Crear un nuevo usuario con validaciones estrictas.
- Actualizar completamente un usuario (PUT).
- Actualizar parcialmente un usuario (PATCH).
- Eliminar un usuario (DELETE).

La API utiliza **FastAPI** y **Pydantic** para validación automática, **HTTPException** para manejo de errores, **Dependency Injection** (`Depends()`) para reutilizar lógica común, y genera documentación interactiva en **Swagger UI** y **ReDoc**.

## Tecnologías utilizadas

- **Python 3.13**
- **FastAPI** – framework web asíncrono
- **Uvicorn** – servidor ASGI
- **Pydantic** – validación de datos y modelos
- **email-validator** – validación de emails

## Instalación de dependencias

### Requisitos previos
- Python 3.13 instalado
- `pip` actualizado

### Pasos

1. **Clonar o crear el proyecto** (estructura ya definida).

2. **Crear y activar un entorno virtual** (recomendado):

```bash
# En la raíz del proyecto device_systems/
python -m venv env

# Activar en Windows (PowerShell)
env\Scripts\Activate.ps1

# Activar en macOS/Linux
source env/bin/activate
```

3. **Instalar dependencias** desde `requirements.txt`:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` debe contener:

```
fastapi==0.115.0
uvicorn[standard]==0.31.0
email-validator>=2.0.0
```

4. **Verificar instalación**:

```bash
pip show fastapi uvicorn
```

## Ejecución del servidor

Con el entorno virtual activado y estando en la carpeta raíz (`device_systems/`), ejecuta:

```bash
uvicorn app.main:app --reload
```

- `--reload` permite recarga automática al detectar cambios.
- El servidor se iniciará en `http://127.0.0.1:8000`.

Para detenerlo: `Ctrl + C`.

## Tabla de endpoints

| Método | Endpoint                     | Descripción                                          | Código de éxito |
|--------|------------------------------|------------------------------------------------------|-----------------|
| GET    | `/`                          | Mensaje de bienvenida y enlace a documentación.      | 200 OK          |
| GET    | `/users`                     | Lista todos los usuarios (filtros opcionales).       | 200 OK          |
| GET    | `/users/{user_id}`           | Obtiene un usuario por su ID.                        | 200 OK          |
| POST   | `/users`                     | Crea un nuevo usuario.                               | 201 Created     |
| PUT    | `/users/{user_id}`           | Reemplaza completamente un usuario existente.        | 200 OK          |
| PATCH  | `/users/{user_id}`           | Actualiza parcialmente un usuario (solo campos enviados). | 200 OK      |
| DELETE | `/users/{user_id}`           | Elimina un usuario.                                  | 204 No Content  |

## Ejemplos de peticiones y respuestas

### GET /users – Listar usuarios con filtros

**Petición:**
```bash
curl -X GET "http://localhost:8000/users?role=admin&is_active=true"
```

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Ana López",
    "email": "ana@example.com",
    "role": "admin",
    "is_active": true
  }
]
```

### GET /users/{user_id} – Obtener usuario por ID

**Petición:**
```bash
curl -X GET "http://localhost:8000/users/1"
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "name": "Ana López",
  "email": "ana@example.com",
  "role": "admin",
  "is_active": true
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Usuario con ID 999 no encontrado"
}
```

### POST /users – Crear usuario

**Petición:**
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carlos Pérez",
    "email": "carlos@example.com",
    "role": "user",
    "is_active": true
  }'
```

**Respuesta (201 Created):**
```json
{
  "id": 2,
  "name": "Carlos Pérez",
  "email": "carlos@example.com",
  "role": "user",
  "is_active": true
}
```

**Error por email duplicado (400 Bad Request):**
```json
{
  "detail": "El correo electrónico ya está registrado"
}
```

**Error por datos inválidos (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "name"],
      "msg": "String should have at least 3 characters",
      "input": "Ab"
    }
  ]
}
```

### PUT /users/{user_id} – Actualización completa

**Petición (reemplaza todo el usuario):**
```bash
curl -X PUT "http://localhost:8000/users/2" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carlos Gómez",
    "email": "carlos.gomez@example.com",
    "role": "support",
    "is_active": false
  }'
```

**Respuesta (200 OK):**
```json
{
  "id": 2,
  "name": "Carlos Gómez",
  "email": "carlos.gomez@example.com",
  "role": "support",
  "is_active": false
}
```

### PATCH /users/{user_id} – Actualización parcial

**Petición (solo cambia el rol):**
```bash
curl -X PATCH "http://localhost:8000/users/2" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin"
  }'
```

**Respuesta (200 OK):**
```json
{
  "id": 2,
  "name": "Carlos Gómez",
  "email": "carlos.gomez@example.com",
  "role": "admin",
  "is_active": false
}
```

**Error si no se envía ningún campo (400 Bad Request):**
```json
{
  "detail": "Debe enviar al menos un campo para actualizar"
}
```

### DELETE /users/{user_id} – Eliminar usuario

**Petición:**
```bash
curl -X DELETE "http://localhost:8000/users/2"
```

**Respuesta (204 No Content):** *sin cuerpo*

**Error si el usuario no existe (404 Not Found):**
```json
{
  "detail": "Usuario no encontrado"
}
```

## Códigos de estado usados

| Código | Significado                          | Cuándo se usa                                                                 |
|--------|--------------------------------------|-------------------------------------------------------------------------------|
| 200    | OK                                   | GET, PUT, PATCH exitosos.                                                     |
| 201    | Created                              | POST exitoso (usuario creado).                                               |
| 204    | No Content                           | DELETE exitoso (sin cuerpo de respuesta).                                    |
| 400    | Bad Request                          | Email duplicado, PATCH sin datos, validaciones de negocio.                   |
| 404    | Not Found                            | Usuario no encontrado por ID.                                                |
| 422    | Unprocessable Entity                 | Datos de entrada no cumplen validaciones de Pydantic (tipo, formato, longitud). |

## Capturas de Swagger UI

**Ejemplo de vista general de endpoints:**

![Swagger UI - Endpoints](/images/swagger-endpoints.png)

## Capturas Pruebas Funcionales


**GET /users – listar**
**Con filtros: ?role=admin&is_active=true**

![GET /users – listar](/images/userlistar.png)

**GET /users/1 – obtener por ID**

![GET /users/1 – obtener por ID](/images/obtenerid.png)

**POST /users – crear**

![POST /users – crear](/images/userscrear.png)

**PUT /users/1 – actualización completa**

![PUT /users/1](/images/actualizacioncompleta.png)

**PATCH /users/1 – actualización parcial**

![PATCH /users/1](/images/actualizacionparcial.png)

**DELETE /users/1 – eliminar**

![DELETE /users/1](/images/deleteuser.png)



# Escenarios de error obligatorios:

**Buscar usuario inexistente → GET /users/999 → 404**

![Buscar usuario inexistente - 404](/images/eo404.png)

**Crear usuario con correo repetido → POST con email ya usado → 400**

![Crear usuario con correo repetido - 400](/images/eo400.png)

**Crear usuario con datos inválidos (ej. name="ab") → 422**

![Crear usuario con datos inválidos - 422](/images/eo422.png)

**Actualizar usuario inexistente (PUT/PATCH con ID inválido) → 404**

![Actualizar usuario inexistente - 404](/images/eo404put.png)

**PATCH vacío (enviar {}) → 400**

![PATCH vacío - 400](/images/eo400patch.png)

**Eliminar usuario inexistente → DELETE /users/999 → 404**

![Eliminar usuario inexistente - 404](/images/eo404delete.png)

## Uso de Dependency Injection con Depends()

FastAPI permite **inyectar dependencias** reutilizables en los endpoints usando la función `Depends()`. En este proyecto, las dependencias se definen en `app/dependencies/user_dependencies.py` y se usan en las rutas para evitar duplicar lógica común.

### Ejemplo de dependencia implementada:

```python
def get_user_or_404(user_id: int, db: list):
    for user in db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado")
```

Esta función se puede inyectar en cualquier endpoint que necesite recuperar un usuario por ID, lanzando automáticamente un error 404 si no existe.

### Uso en la ruta (aunque en el código se llamó manualmente, la idea conceptual es):

```python
@router.get("/{user_id}")
def get_user(user: dict = Depends(lambda: get_user_or_404(user_id, fake_db))):
    return user
```

Las dependencias permiten:
- **Reutilizar** validaciones (email duplicado, rol permitido).
- **Centralizar** la lógica de acceso a datos.
- **Mejorar la testabilidad** (se pueden simular dependencias en pruebas).
- **Mantener el código limpio** y enfocado en la lógica de negocio.

## Manejo de errores implementado

Se utiliza `HTTPException` de FastAPI para devolver respuestas de error con códigos HTTP apropiados. Los casos controlados son:

1. **Usuario no encontrado** (cualquier operación por ID) → `404 Not Found`.
2. **Correo electrónico duplicado** (POST o PUT con email ya existente) → `400 Bad Request`.
3. **Rol no permitido** (lo valida automáticamente Pydantic con Enum, devuelve 422).
4. **Intento de actualización sin datos** (PATCH con cuerpo vacío) → `400 Bad Request`.
5. **Datos con formato inválido** (ej. name muy corto, email mal formado) → `422 Unprocessable Entity`.

Ejemplo de respuesta de error estructurada (por defecto FastAPI):

```json
{
  "detail": "El correo electrónico ya está registrado"
}
```

Opcionalmente, se pueden personalizar para devolver más contexto (no implementado en esta versión base).

## Link del video

https://www.loom.com/share/b0a7c7fdb33d4d8eac7cad4304c5b8fe


### Fast API SQL ALCHEMY

## device_systems API

API REST completa para la gestión de usuarios del sistema **device_systems**.  
Permite operaciones CRUD con validaciones, filtros, manejo de errores y documentación interactiva automática.

# Tecnologías utilizadas

- Python 3.13
- FastAPI 0.115.0
- Uvicorn (servidor ASGI)
- Pydantic (validación de datos)
- email-validator

# Instalación de dependencias

```bash
python -m venv env
source env/bin/activate  # o env\Scripts\activate en Windows
pip install -r requirements.txt
```

# Ejecutar el servidor

```bash

uvicorn app.main:app --reload

```

## Ejemplos de peticiones y respuestas

# 1. Crear un usuario válido.

![Crear usuario válido](/images/alch1.png)

# 2. Intentar crear un usuario con email repetido.

![Crear un usuario con email repetido](/images/alch2.png)

# 3. Listar usuarios.

![Listar usuarios](/images/alch3.png)

# 4. Consultar usuario por ID.

![Consultar usuario por ID](/images/alch4.png)

# 5. Consultar usuario inexistente.

![Consultar usuario inexistente](/images/alch5.png)

# 6. Filtrar usuarios por rol.

![Filtrar usuarios por rol](/images/alch6.png)

# 7. Filtrar usuarios activos.

![Filtrar usuarios activos](/images/alch7.png)

# 8. Actualizar usuario completo con PUT.

![Actualizar usuario completo con PUT](/images/alch8.png)

# 9. Actualizar parcialmente un usuario con PATCH.

![Actualizar parcialmente un usuario con PATCH](/images/alch9.png)

# 10. Eliminar usuario con DELETE.

![Eliminar usuario con DELETE](/images/alch10.png)

# 11. Validar que el usuario eliminado ya no exista.

![Validar que el usuario eliminado ya no exista](/images/alch11.png)


### Link del video

