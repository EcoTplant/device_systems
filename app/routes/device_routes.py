from fastapi import APIRouter, Depends, Query, status, HTTPException, Request
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services import device_service
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support, require_admin
from app.models.user_model import User
from app.main import limiter

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/", response_model=List[DeviceResponse])
@limiter.limit("30/minute")
def get_devices(
    request: Request,
    device_type: Optional[str] = Query(None, description="Tipo de dispositivo"),
    is_available: Optional[bool] = Query(None, description="Disponibilidad"),
    brand: Optional[str] = Query(None, description="Marca"),
    search: Optional[str] = Query(None, description="Búsqueda por nombre o serie"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # Autenticado
):
    """Lista dispositivos con filtros (requiere autenticación)."""
    return device_service.get_all_devices(db, device_type, is_available, brand, search)

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # Autenticado
):
    """Obtiene un dispositivo por ID (requiere autenticación)."""
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)  # Admin o Support
):
    """Crea un nuevo dispositivo (requiere admin o support)."""
    return device_service.create_device(db, device_data)

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)  # Admin o Support
):
    """Actualiza completamente un dispositivo (requiere admin o support)."""
    return device_service.update_device(db, device_id, device_data)

@router.patch("/{device_id}", response_model=DeviceResponse)
def patch_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)  # Admin o Support
):
    """Actualiza parcialmente un dispositivo (requiere admin o support)."""
    return device_service.update_device(db, device_id, device_data)

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)  # Solo Admin
):
    """Elimina un dispositivo (requiere rol admin)."""
    device_service.delete_device(db, device_id)
    return None