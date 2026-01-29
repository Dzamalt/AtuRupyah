from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Numeric, ForeignKey, Date

from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)

    # Optional: backref to products if you want easy access
    products: Mapped[List["Product"]] = relationship("Product", back_populates="user")


class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    name: Mapped[str] = mapped_column(String(80), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(10,2), nullable=False)

    # Relationships
    inventory: Mapped[Optional["Inventory"]] = relationship(
        "Inventory",
        back_populates="product",
        uselist=False,
        passive_deletes=True
    )

    sales: Mapped[List["Sale"]] = relationship(
        "Sale",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    user: Mapped["User"] = relationship("User", back_populates="products")


class Inventory(db.Model):
    __tablename__ = 'inventories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    reorder_level: Mapped[int] = mapped_column(Integer, nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="inventory")


class Sale(db.Model):
    __tablename__ = 'sales'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)

    quantity_sold: Mapped[int] = mapped_column(Integer, nullable=False)
    sale_date: Mapped[Date] = mapped_column(Date, nullable=False)
    price_at_sale: Mapped[Numeric] = mapped_column(Numeric(10,2), nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="sales")
