from fastapi import APIRouter, Depends, Query, status, HTTPException, Request
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.loan_schema import LoanCreate, LoanUpdate, LoanResponse, LoanDetailResponse
from app.services import loan_service, user_service, device_service
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support
from app.models.user_model import User
from app.rate_limit import limiter

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.get("/", response_model=List[LoanResponse])
@limiter.limit("30/minute")
def get_loans(
    request: Request,
    status_filter: Optional[str] = Query(None, description="Estado del préstamo"),
    user_email: Optional[str] = Query(None, description="Email del usuario"),
    device_type: Optional[str] = Query(None, description="Tipo de dispositivo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # Autenticado
):
    """Lista préstamos con filtros (requiere autenticación)."""
    return loan_service.get_all_loans(db, status_filter, user_email, device_type)

@router.get("/details", response_model=List[LoanDetailResponse])
@limiter.limit("30/minute")
def get_loan_details(
    request: Request,
    status_filter: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    device_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)  # Admin o Support
):
    """Obtiene préstamos con datos de usuario y dispositivo anidados (requiere admin o support)."""
    loans = loan_service.get_all_loans(db, status_filter, user_email, device_type)
    result = []
    for loan in loans:
        user = user_service.get_user_by_id(db, loan.user_id)
        device = device_service.get_device_by_id(db, loan.device_id)
        result.append({
            "loan_id": loan.id,
            "status": loan.status,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date,
            "user": user,
            "device": device
        })
    return result

@router.get("/{loan_id}", response_model=LoanDetailResponse)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)  # Admin o Support
):
    """Obtiene un préstamo por ID con datos anidados (requiere admin o support)."""
    loan = loan_service.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    user = user_service.get_user_by_id(db, loan.user_id)
    device = device_service.get_device_by_id(db, loan.device_id)
    return {
        "loan_id": loan.id,
        "status": loan.status,
        "loan_date": loan.loan_date,
        "return_date": loan.return_date,
        "user": user,
        "device": device
    }

@router.get("/user/{user_id}", response_model=List[LoanResponse])
def get_loans_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # Autenticado
):
    """Obtiene todos los préstamos de un usuario (requiere autenticación)."""
    return loan_service.get_loans_by_user(db, user_id)

@router.get("/device/{device_id}", response_model=List[LoanResponse])
def get_loans_by_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)  # Admin o Support
):
    """Obtiene historial de préstamos de un dispositivo (requiere admin o support)."""
    return loan_service.get_loans_by_device(db, device_id)

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_loan(
    request: Request,
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # Autenticado
):
    """Crea un nuevo préstamo (requiere autenticación)."""
    return loan_service.create_loan(db, loan_data)

@router.patch("/{loan_id}/return", response_model=LoanResponse)
def return_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)  # Admin o Support
):
    """Registra la devolución de un préstamo (requiere admin o support)."""
    return loan_service.return_loan(db, loan_id)