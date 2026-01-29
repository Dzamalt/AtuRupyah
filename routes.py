from flask import Blueprint, render_template
from datetime import datetime

from services import add_stock, create_sale

#temporary
from models import User, Product, Inventory, Sale
from extensions import db
from services import product_convertible, is_low_stock
from analytics import (load_sales_df, total_units_sold, total_revenue,top_products,daily_sales)



bp = Blueprint("main", __name__)

@bp.route('/')
def hello_world():
    return 'Hello World!'

@bp.route('/add_product')
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


@bp.route('/see_product')
def see_product():
    result = db.session.execute(db.select(Product))
    all_products = [product_convertible(item) for item in result.scalars()]
    for product in all_products:
        product["lowstock"] = is_low_stock(product["id"])
    return render_template("see_product_test.html", all_products=all_products)


@bp.route('/edit_product')
def edit_product():
    product = db.session.query(Product).order_by(Product.id.desc()).first()
    product.name = "LaptopMSI"
    db.session.commit()
    return 'Hello World! Product edit successfully'


@bp.route('/delete_product')
def delete_product():
    product = db.session.query(Product).order_by(Product.id.desc()).first()
    db.session.delete(product)

    db.session.commit()
    return 'Hello World! Product deleted successfully'

@bp.route("/add_stock/<int:pid>/<int:amount>")
def add_stock_route(pid, amount):
    add_stock(pid, amount)
    return "Hello World! Stock added"


@bp.route("/make_sale/<int:pid>/<int:amount>")
def sale_route(pid, amount):
    create_sale(pid, amount, datetime.now().date())
    return "Hello World! Sale created"


@bp.route("/analytics")
def analytics_dashboard():
    df = load_sales_df()
    total_sold = total_units_sold(df)
    total_sale = total_revenue(df)
    best_product = top_products(df)
    sale_daily = daily_sales(df)
    return {
        "total_sold": total_sold,
        "total_sale": total_sale,
        "best_product": best_product.to_dict(),
        "sale_daily": sale_daily,
    }

