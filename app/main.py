from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes import user_routes, device_routes, loan_routes
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.request_middleware import RequestMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(RequestMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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