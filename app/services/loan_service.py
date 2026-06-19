from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.loan_model import Loan
from app.models.device_model import Device
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate, LoanUpdate
from datetime import datetime
from typing import Optional

def get_all_loans(db: Session, status_filter: Optional[str] = None,
                  user_email: Optional[str] = None,
                  device_type: Optional[str] = None):
    query = db.query(Loan)
    if status_filter:
        query = query.filter(Loan.status == status_filter)
    if user_email:
        query = query.join(Loan.user).filter(User.email == user_email)
    if device_type:
        query = query.join(Loan.device).filter(Device.device_type == device_type)
    return query.all()

def get_loan_by_id(db: Session, loan_id: int):
    return db.query(Loan).filter(Loan.id == loan_id).first()

def get_loans_by_user(db: Session, user_id: int):
    return db.query(Loan).filter(Loan.user_id == user_id).all()

def get_loans_by_device(db: Session, device_id: int):
    return db.query(Loan).filter(Loan.device_id == device_id).all()

def create_loan(db: Session, loan_data: LoanCreate):
    # Validar usuario
    user = db.query(User).filter(User.id == loan_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Validar dispositivo
    device = db.query(Device).filter(Device.id == loan_data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if not device.is_available:
        raise HTTPException(status_code=409, detail="Dispositivo no disponible")
    # Crear préstamo
    new_loan = Loan(user_id=loan_data.user_id, device_id=loan_data.device_id, status="active")
    db.add(new_loan)
    # Marcar dispositivo como no disponible
    device.is_available = False
    db.commit()
    db.refresh(new_loan)
    return new_loan

def return_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if loan.status == "returned":
        raise HTTPException(status_code=400, detail="Préstamo ya devuelto")
    loan.status = "returned"
    loan.return_date = datetime.now()
    # Liberar dispositivo
    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan

def update_loan(db: Session, loan_id: int, loan_update: LoanUpdate):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    update_data = loan_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(loan, field, value)
    db.commit()
    db.refresh(loan)
    return loan