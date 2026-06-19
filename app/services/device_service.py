from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate
from typing import Optional

def get_all_devices(db: Session, device_type: Optional[str] = None,
                    is_available: Optional[bool] = None,
                    brand: Optional[str] = None,
                    search: Optional[str] = None):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            (Device.name.ilike(f"%{search}%")) |
            (Device.serial_number.ilike(f"%{search}%"))
        )
    return query.all()

def get_device_by_id(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()

def create_device(db: Session, device_data: DeviceCreate):
    existing = db.query(Device).filter(Device.serial_number == device_data.serial_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Número de serie ya registrado")
    new_device = Device(**device_data.model_dump())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

def update_device(db: Session, device_id: int, device_update: DeviceUpdate):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    update_data = device_update.model_dump(exclude_unset=True)
    if "serial_number" in update_data:
        existing = db.query(Device).filter(
            Device.serial_number == update_data["serial_number"],
            Device.id != device_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Número de serie ya registrado")
    for field, value in update_data.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device

def delete_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    db.delete(device)
    db.commit()
    return True