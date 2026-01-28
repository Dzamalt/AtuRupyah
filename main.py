from datetime import date, datetime
from typing import List, Optional

from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, event, ForeignKey, Date, Numeric
from sqlalchemy.engine import Engine
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from dotenv import load_dotenv
from forms import LoginForm, RegisterForm

load_dotenv()





@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

def inventory_convertible(inventory):
    return {
        "id": inventory.id,
        "product_id": inventory.product_id,
        "quantity": inventory.quantity,
        "reorder_level": inventory.reorder_level,
    }

def sale_convertible(sale):
    return {
        "id": sale.id,
        "product_id": sale.product_id,
        "quantity_sold": sale.quantity_sold,
        "sale_date": sale.sale_date,
        "price_at_sale": sale.price_at_sale,
    }

def product_convertible(item):
    return {
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'price': float(item.price),
        'inventory': inventory_convertible(item.inventory) if item.inventory else None,
        'sale': [sale_convertible(s) for s in item.sales]
    }

ckeditor = CKEditor(app)
Bootstrap5(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"
# ^Uncomment when adding users

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

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





with app.app_context():
    db.drop_all()
    db.create_all()


# with app.app_context():



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/add_product')
def add_product():
    user = User(
        username = "bihi",
        password = "12345",
        email = "dzam@ggwp.com"
    )
    db.session.add(user)
    db.session.commit()
    product = Product(
        user_id=1,
        name="Laptop",
        category="Electronics",
        price=1200.00
    )
    db.session.add(product),
    db.session.commit()
    inventory = Inventory(
        product_id=product.id,
        quantity=20,
        reorder_level=5
    )
    db.session.add(inventory)
    db.session.commit()
    custom_date = datetime(2026, 1, 15, 14, 30)
    sale = Sale(
        product=product,
        quantity_sold=3,
        price_at_sale=product.price,
        sale_date=custom_date
    )

    db.session.add(sale)
    db.session.commit()
    custom_date1 = datetime(2026, 2, 16, 15, 31)
    sale1 = Sale(
        product=product,
        quantity_sold=4,
        price_at_sale=product.price,
        sale_date=custom_date1
    )

    db.session.add(sale1)
    db.session.commit()
    print("added product")
    return "Hello World! Product added successfully"


@app.route('/see_product')
def see_product():
    result = db.session.execute(db.select(Product))
    all_products = [product_convertible(item) for item in result.scalars()]
    return render_template("see_product_test.html", all_products=all_products)


@app.route('/edit_product')
def edit_product():
    product = db.session.query(Product).order_by(Product.id.desc()).first()
    product.name = "LaptopMSI"
    db.session.commit()
    return 'Hello World! Product edit successfully'


@app.route('/delete_product')
def delete_product():
    product = db.session.query(Product).order_by(Product.id.desc()).first()
    db.session.delete(product)

    db.session.commit()
    return 'Hello World! Product deleted successfully'




# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    app.run(debug=True, port=5002)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
