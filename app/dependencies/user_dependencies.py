from fastapi import HTTPException, status, Depends
from app.schemas.user_schema import UserRole

# Simulador de base de datos (importado desde rutas, pero lo manejamos con referencia)
# Para evitar importaciones circulares, pasaremos la db como parámetro o usaremos un módulo común.
# Aquí definimos funciones que reciben la db desde la ruta (inyección manual simplificada).

def get_user_or_404(user_id: int, db: list):
    """Busca un usuario por ID, si no existe lanza 404."""
    for user in db:
        if user["id"] == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con ID {user_id} no encontrado"
    )

def check_email_duplicate(email: str, db: list, exclude_user_id: int = None):
    """Verifica si el email ya existe en la db, excluyendo opcionalmente un ID."""
    for user in db:
        if user["email"] == email and (exclude_user_id is None or user["id"] != exclude_user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado"
            )
    return email

def validate_role(role: UserRole):
    """Valida que el rol sea permitido (ya lo hace Pydantic, pero ejemplo de dependencia)."""
    # El modelo ya valida mediante Enum, pero podemos agregar lógica extra
    return role