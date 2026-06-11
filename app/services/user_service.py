from fastapi import HTTPException, status
from app.data.users_db import fake_db, current_id as _current_id
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse

# Para mantener el ID global, usa una variable global mutable
# (simulamos un contador, pero en una BD real sería automático)
current_id = _current_id

def get_all_users(role=None, is_active=None):
    result = fake_db.copy()
    if role:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result

def get_user_by_id(user_id: int):
    for user in fake_db:
        if user["id"] == user_id:
            return user
    return None

def create_user(user_data: UserCreate):
    global current_id
    # Verificar email duplicado
    for user in fake_db:
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado"
            )
    new_user = user_data.model_dump()
    new_user["id"] = current_id
    current_id += 1
    fake_db.append(new_user)
    return new_user

def update_user_full(user_id: int, user_data: UserCreate):
    # Buscar índice
    index = None
    for i, user in enumerate(fake_db):
        if user["id"] == user_id:
            index = i
            break
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    # Verificar email duplicado (excluyendo este usuario)
    for user in fake_db:
        if user["email"] == user_data.email and user["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado por otro usuario"
            )
    updated_user = user_data.model_dump()
    updated_user["id"] = user_id
    fake_db[index] = updated_user
    return updated_user

def update_user_partial(user_id: int, user_update: UserUpdate):
    index = None
    for i, user in enumerate(fake_db):
        if user["id"] == user_id:
            index = i
            break
    if index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = user_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar"
        )
    # Si se actualiza email, verificar duplicado
    if "email" in update_data:
        for user in fake_db:
            if user["email"] == update_data["email"] and user["id"] != user_id:
                raise HTTPException(
                    status_code=400,
                    detail="El correo electrónico ya está registrado por otro usuario"
                )
    current_user = fake_db[index]
    for field, value in update_data.items():
        current_user[field] = value
    fake_db[index] = current_user
    return current_user

def delete_user(user_id: int):
    index = None
    for i, user in enumerate(fake_db):
        if user["id"] == user_id:
            index = i
            break
    if index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    fake_db.pop(index)
    return True