from fastapi import FastAPI
from app.routes import user_routes

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems.\n\n"
                "Operaciones CRUD completas con validaciones, filtros y manejo de errores.",
    version="3.0.0",
    contact={
        "name": "Soporte device_systems",
        "email": "soporte@devicesystems.com",  # sin guión bajo
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir rutas
app.include_router(user_routes.router)

# Middleware opcional para cabeceras personalizadas
@app.middleware("http")
async def add_custom_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "3.0"
    return response

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a device_systems API", "docs": "/docs"}