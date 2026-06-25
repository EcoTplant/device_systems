# app/auth/auth_routes.py
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.auth_schema import UserRegister, UserLogin, Token, UserAuthResponse
from app.services.auth_service import register_user, authenticate_user
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User
from app.rate_limit import limiter  # <-- Importar limiter
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserAuthResponse, status_code=201)
@limiter.limit("3/minute")
def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    return register_user(db, user_data)

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(
    request: Request,
    user_creds: UserLogin,
    db: Session = Depends(get_db)
):
    access_token = authenticate_user(db, user_creds.email, user_creds.password)
    if not access_token:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserAuthResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user