from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from enum import Enum

# Enumeración para roles permitidos
class UserRole(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

# Modelo para crear usuario (entrada)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre completo, mínimo 3 caracteres")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    role: UserRole = Field(default=UserRole.user, description="Rol del usuario")
    is_active: bool = Field(default=True, description="Estado activo/inactivo")

# Modelo para respuesta (lo que se devuelve al cliente)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        # Permite convertir desde diccionario o desde objeto ORM
        from_attributes = True

# Modelo interno para almacenar usuarios (similar a UserResponse pero con Optional para ID)
class UserInDB(UserResponse):
    pass  # Podríamos añadir más campos internos si fuera necesario