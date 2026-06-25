# app/routes/user_routes.py
from fastapi import APIRouter, Depends, Query, status, Request, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserRole
from app.services import user_service
from app.rate_limit import limiter
from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_admin_or_support,
    require_admin        # <-- importar esta función
)
from app.models.user_model import User
from app.rate_limit import limiter  # <-- importar desde rate_limit

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
@limiter.limit("30/minute")
def get_users(
    request: Request,
    role: Optional[UserRole] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return user_service.get_all_users(db, role=role, is_active=is_active)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    return user_service.create_user(db, user_data)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_full(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    return user_service.update_user_full(db, user_id, user_data)

@router.patch("/{user_id}", response_model=UserResponse)
def update_user_partial(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    return user_service.update_user_partial(db, user_id, user_update)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)  # <-- ahora sí está importado
):
    user_service.delete_user(db, user_id)
    return None