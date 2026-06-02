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
