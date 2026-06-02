from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

# Modelo para crear (POST) y actualización completa (PUT)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre completo, mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    role: UserRole = Field(default=UserRole.user, description="Rol del usuario")
    is_active: bool = Field(default=True, description="Estado activo/inactivo")

# Modelo para actualización parcial (PATCH) – todos opcionales
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# Modelo de respuesta (lo que se devuelve al cliente)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True