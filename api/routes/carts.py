from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.cart import Cart, CartItem
from api.models.product import Product
from api.models.user import User
from api.schemas.cart import CartItemCreate, CartItemUpdate, CartItemOut
from api.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=list[CartItemOut])
async def get_user_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        return []

    return cart.items  # SQLAlchemy maneja la relación

@router.post("/items", response_model=CartItemOut, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    item_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Obtener o crear el carrito
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Verificar que el producto existe
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar si el ítem ya está en el carrito
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item_data.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.put("/items/{item_id}", response_model=CartItemOut)
async def update_cart_item(
    item_id: int,
    update_data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.id == item_id,
        Cart.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    cart_item.quantity = update_data.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.id == item_id,
        Cart.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    db.delete(cart_item)
    db.commit()
    return

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        return

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return

