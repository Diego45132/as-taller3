from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, products, carts

# ✅ Crear la instancia de FastAPI
app = FastAPI(
    title="Tienda Virtual API",
    version="1.0.0",
    description="API para una tienda en línea con gestión de usuarios, productos y carrito de compras."
)

# ✅ Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # frontend local
    "http://127.0.0.1:3000",
    "https://mi-tienda-frontend.com",  # producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # puedes usar ["*"] en desarrollo
    allow_credentials=True,
    allow_methods=["*"],            # permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],            # permite todos los encabezados
)

# ✅ Incluir los routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(carts.router, prefix="/api/v1/carts", tags=["carts"])

# ✅ Endpoint raíz de prueba
@app.get("/")
async def root():
    return {"message": "Tienda Virtual API"}

# ✅ Endpoint de verificación de salud
@app.get("/health")
async def health_check():
    return {"status": "ok"}
