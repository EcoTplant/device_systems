from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserRole, UserUpdate
from app.dependencies.user_dependencies import get_user_or_404, check_email_duplicate

router = APIRouter(prefix="/users", tags=["Users"])

# Base de datos simulada (en memoria)
fake_db = []
current_id = 1

# --- Endpoints ya existentes (GET, POST) ---
@router.get("/", response_model=List[UserResponse])
def get_users(
    role: Optional[UserRole] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo")
):
    result = fake_db.copy()
    if role:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int):
    user = get_user_or_404(user_id, fake_db)
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    # Validar email duplicado
    check_email_duplicate(user_data.email, fake_db)
    global current_id
    new_user = user_data.model_dump()
    new_user["id"] = current_id
    current_id += 1
    fake_db.append(new_user)
    return new_user

# --- NUEVO: PUT (actualización completa) ---
@router.put("/{user_id}", response_model=UserResponse)
def update_user_full(user_id: int, user_data: UserCreate):
    # Buscar usuario
    user_index = None
    for i, user in enumerate(fake_db):
        if user["id"] == user_id:
            user_index = i
            break
    if user_index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Validar email duplicado (excluyendo el mismo usuario)
    check_email_duplicate(user_data.email, fake_db, exclude_user_id=user_id)
    
    # Reemplazar completamente
    updated_user = user_data.model_dump()
    updated_user["id"] = user_id
    fake_db[user_index] = updated_user
    return updated_user

# --- NUEVO: PATCH (actualización parcial) ---
@router.patch("/{user_id}", response_model=UserResponse)
def update_user_partial(user_id: int, user_update: UserUpdate):
    # Buscar usuario
    user_index = None
    for i, user in enumerate(fake_db):
        if user["id"] == user_id:
            user_index = i
            break
    if user_index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Obtener solo los campos enviados (excluir valores None)
    update_data = user_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar"
        )
    
    # Si se actualiza email, validar duplicado (excluyendo este usuario)
    if "email" in update_data:
        check_email_duplicate(update_data["email"], fake_db, exclude_user_id=user_id)
    
    # Aplicar actualizaciones
    current_user = fake_db[user_index]
    for field, value in update_data.items():
        current_user[field] = value
    
    # Actualizar en la lista
    fake_db[user_index] = current_user
    return current_user

# --- NUEVO: DELETE (eliminación) ---
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    user_index = None
    for i, user in enumerate(fake_db):
        if user["id"] == user_id:
            user_index = i
            break
    if user_index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Eliminar de la lista
    fake_db.pop(user_index)
    # Respuesta 204 No Content (sin cuerpo)
    return None