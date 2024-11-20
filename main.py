from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router
from core.config import settings
from db.base import Base
from db.session import engine

app = FastAPI(title="Colecciones Tematicas")

# Configurar los orígenes permitidos (dominios que pueden hacer peticiones al backend)
origins = [
    "http://localhost:3000",  # Dominio de tu aplicación Nuxt
    "http://127.0.0.1:3000",
    "http://172.16.143.6:4000",
    "http://biblio-pruebas.colmex.mx:4000"  # Otra forma de localhost (por si acaso)
]

# Agregar el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estos orígenes
    allow_credentials=True,  # Permitir credenciales como cookies
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Registrar rutas de la API
app.include_router(api_router, prefix=settings.API_V1_STR)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)