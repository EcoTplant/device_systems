from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# URL de conexión a SQLite (archivo físico en la raíz del proyecto)
DATABASE_URL = "sqlite:///./app.db"

# Motor de base de datos
# check_same_thread=False es necesario para SQLite con FastAPI (múltiples hilos)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos ORM
class Base(DeclarativeBase):
    pass

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()