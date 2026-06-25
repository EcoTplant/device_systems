import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings

def _truncate_password(password: str) -> bytes:
    """Trunca la contraseña a 72 bytes (límite de bcrypt)."""
    return password.encode('utf-8')[:72]

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña usando bcrypt."""
    truncated = _truncate_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(truncated, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash bcrypt."""
    truncated = _truncate_password(plain_password)
    return bcrypt.checkpw(truncated, hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None