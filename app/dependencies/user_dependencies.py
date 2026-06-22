"""
Comentamos las dependencias ya que no se usa con base de datos

from fastapi import Depends, HTTPException, status
from app.services.user_service import get_user_by_id
from app.data.users_db import fake_db
from typing import Optional

def get_user_or_404(user_id: int):
    """Dependencia que obtiene un usuario o lanza 404"""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user

def check_email_duplicate(email: str, exclude_user_id: Optional[int] = None):
    """Verifica si el email ya existe en la BD, excluyendo opcionalmente un ID"""
    for user in fake_db:
        if user["email"] == email and (exclude_user_id is None or user["id"] != exclude_user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado"
            )
    return email

    """"