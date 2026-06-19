from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes import user_routes, device_routes, loan_routes

# Crear tablas (en caso de no usar migraciones aún)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios, dispositivos y préstamos",
    version="3.0.0",
    contact={
        "name": "Soporte device_systems",
        "email": "soporte@devicesystems.com",
    },
)

app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)

@app.get("/")
def root():
    return {"message": "device_systems API v3", "docs": "/docs"}