from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserRole, UserUpdate
from app.services import user_service
from app.dependencies.user_dependencies import get_user_or_404, check_email_duplicate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
def get_users(
    role: Optional[UserRole] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo")
):
    """Lista todos los usuarios con filtros opcionales"""
    return user_service.get_all_users(role=role, is_active=is_active)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user=Depends(get_user_or_404)):
    """Obtiene un usuario por su ID"""
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    """Crea un nuevo usuario"""
    return user_service.create_user(user_data)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_full(user_id: int, user_data: UserCreate):
    """Reemplaza completamente un usuario existente"""
    return user_service.update_user_full(user_id, user_data)

@router.patch("/{user_id}", response_model=UserResponse)
def update_user_partial(user_id: int, user_update: UserUpdate):
    """Actualiza parcialmente un usuario (solo campos enviados)"""
    return user_service.update_user_partial(user_id, user_update)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Elimina un usuario existente"""
    user_service.delete_user(user_id)
    return None  # 204 No Content no tiene cuerpo