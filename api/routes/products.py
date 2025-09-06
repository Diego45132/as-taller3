from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product, ProductCreate, ProductUpdate, ProductOut
from typing import List
from fastapi import Request

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/destacados")
async def productos_destacados(db: Session = Depends(get_db)):
    # Verificar si hay productos en la base de datos
    product_count = db.query(Product).count()
    
    # Si no hay productos, insertar algunos de prueba
    if product_count == 0:
        productos_prueba = [
            {
                "name": "Camiseta Azul Premium",
                "description": "Camiseta 100% algodón orgánico, cómoda y suave",
                "price": 19.99,
                "stock": 50,
                "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop"
            },
            {
                "name": "Pantalón Negro Elegante",
                "description": "Pantalón de vestir negro, perfecto para ocasiones formales",
                "price": 39.99,
                "stock": 20,
                "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=400&fit=crop"
            },
            {
                "name": "Zapatillas Deportivas",
                "description": "Zapatillas cómodas para correr y hacer ejercicio",
                "price": 59.99,
                "stock": 15,
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop"
            },
            {
                "name": "Chaqueta de Cuero",
                "description": "Chaqueta de cuero genuino, estilo clásico y duradero",
                "price": 89.99,
                "stock": 10,
                "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop"
            },
            {
                "name": "Reloj Inteligente",
                "description": "Reloj inteligente con GPS, monitor de frecuencia cardíaca y notificaciones",
                "price": 199.99,
                "stock": 25,
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop"
            },
            {
                "name": "Auriculares Inalámbricos",
                "description": "Auriculares con cancelación de ruido y sonido de alta calidad",
                "price": 79.99,
                "stock": 30,
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop"
            }
        ]
        
        for producto_data in productos_prueba:
            producto = Product(**producto_data)
            db.add(producto)
        db.commit()
    
    # Obtener los primeros 6 productos como destacados
    products = db.query(Product).limit(6).all()
    
    # Convertir a formato compatible con el frontend
    productos_destacados = []
    for product in products:
        productos_destacados.append({
            "id": product.id,
            "nombre": product.name,
            "descripcion": product.description or "Sin descripción",
            "precio": float(product.price),
            "image_url": product.image_url or "https://via.placeholder.com/400x400?text=Sin+Imagen"
        })
    
    return productos_destacados

@router.get("/featured", response_model=List[ProductOut])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    product_url = request.url_for("get_product", product_id=product_id)
    print(f"Product URL: {product_url}")
    
    return product

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # si usas auth
):
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(product)
    db.commit()
