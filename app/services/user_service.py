# app/services/user_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from typing import Optional

# === GET ALL ===
def get_all_users(db: Session, role: Optional[str] = None, is_active: Optional[bool] = None):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()

# === GET BY ID ===
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# === GET BY EMAIL (para autenticación) ===
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# === CREATE (admin o support) ===
def create_user(db: Session, user_data: UserCreate):
    # Verificar email único
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=user_data.hashed_password,  # Debe venir ya hasheado
        role=user_data.role if user_data.role else "user",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# === UPDATE FULL ===
def update_user_full(db: Session, user_id: int, user_data: UserCreate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Verificar email duplicado (excluyendo este usuario)
    existing = db.query(User).filter(User.email == user_data.email, User.id != user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado por otro usuario")
    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active if hasattr(user_data, 'is_active') else True
    # Si se envía una nueva contraseña, hashearla y actualizar
    if hasattr(user_data, 'password') and user_data.password:
        from app.auth.security import get_password_hash
        user.hashed_password = get_password_hash(user_data.password)
    db.commit()
    db.refresh(user)
    return user

# === UPDATE PARTIAL ===
def update_user_partial(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    update_data = user_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo")
    # Si se actualiza email, verificar duplicado
    if "email" in update_data:
        existing = db.query(User).filter(User.email == update_data["email"], User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email ya registrado por otro usuario")
    # Si se actualiza password, hashearla
    if "password" in update_data:
        from app.auth.security import get_password_hash
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

# === DELETE ===
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return True