from fastapi import APIRouter, HTTPException, Query, status, Response
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserRole

# Simulador de base de datos (en memoria)
fake_db = []
current_id = 1

router = APIRouter(prefix="/users", tags=["Usuarios"])

# Endpoint GET /users (listar todos, con filtros query)
@router.get("/", response_model=List[UserResponse])
def get_users(
    role: Optional[UserRole] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo")
):
    """
    Obtiene la lista de usuarios. Permite filtrar por 'role' y/o 'is_active'.
    """
    result = fake_db.copy()
    if role:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result

# Endpoint GET /users/{user_id}
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int):
    """
    Obtiene un usuario por su ID (path parameter).
    """
    user = next((u for u in fake_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Endpoint POST /users
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    global current_id
    # Validar email duplicado
    existing = next((u for u in fake_db if u["email"] == user_data.email), None)
    if existing:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    
    # Crear nuevo usuario (asignar ID)
    new_user = user_data.model_dump()   # Convierte a dict
    new_user["id"] = current_id
    current_id += 1
    fake_db.append(new_user)
    
    # Podemos añadir cabeceras personalizadas (más adelante en main)
    return new_user