from fastapi import FastAPI, Request, Response
from app.routes import user_routes

app = FastAPI(
    title="API de Usuarios - device_systems",
    description="API REST para administrar usuarios del sistema device_systems",
    version="1.0"
)

# Incluir las rutas de usuarios
app.include_router(user_routes.router)

# Middleware para añadir cabeceras personalizadas a todas las respuestas
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return response

# Endpoint raíz opcional (solo información)
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de device_systems", "docs": "/docs"}