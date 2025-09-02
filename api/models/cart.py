from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base  
from pydantic import BaseModel
from typing import Optional



class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int
    user_id: Optional[int] = None 


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None  

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

