# app/schemas/auth_schema.py
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ConfigDict
from typing import Optional
import re

class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Optional[str] = Field("user", pattern="^(admin|support|user)$")

    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe tener al menos una mayúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe tener al menos una minúscula")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe tener al menos un número")
        if " " in v:
            raise ValueError("La contraseña no puede contener espacios")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class UserAuthResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)