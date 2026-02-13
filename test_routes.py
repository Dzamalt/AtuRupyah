from flask import Blueprint, render_template, redirect, request, jsonify
from datetime import datetime

from services import add_stock, create_sale, inventory_convertible, product_convertible, is_low_stock, create_product, \
    sale_convertible, update_forecast

#temporary
from models import User, Product, Inventory, Sale
from extensions import db
from analytics import (load_sales_df, total_units_sold, total_revenue,top_products,daily_sales,moving_average)



bp = Blueprint("main", __name__)

@bp.route('/')
def hello_world():
    return render_template("index.html")

@bp.route('/add_product',methods=['GET','POST'])
def add_product():
    form = None
    if form.validate_on_submit():
        print(form.name.data)
        create_product(
            name=str(form.name.data),
            category=str(form.category.data),
            price=float(form.price.data),
            initial_quantity=int(form.quantity.data),
            reorder_level=int(form.reorder_level.data)
        )
        return redirect("/")
    return render_template("modify_product.html",form=form,is_edit=False)


@bp.route('/see_product')
def see_product():
    result = db.session.execute(db.select(Product))
    all_products = [product_convertible(item,include_inventory=True,include_sale=True) for item in result.scalars()]
    for product in all_products:
        product["lowstock"] = is_low_stock(product["id"])
    print(all_products[0])
    return render_template("see_product_test.html", all_products=all_products)


@bp.route('/edit_product/<int:product_id>',methods=['GET','POST'])
def edit_product(product_id):
    product= db.get_or_404(Product, product_id)
    form = None

    if request.method == 'GET' and product.inventory:
        form.quantity.data = product.inventory.quantity
        form.reorder_level.data = product.inventory.reorder_level
    if form.validate_on_submit():
        product.name = form.name.data
        product.category = form.category.data
        product.price = form.price.data

        product.inventory.quantity = form.quantity.data
        product.inventory.reorder_level = form.reorder_level.data

        db.session.commit()
        return redirect("/")
    return render_template("modify_product.html",form=form,is_edit=True)


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
    update_forecast(2,mtd="update")
    df = load_sales_df()
    total_sold = total_units_sold(df)
    total_sale = total_revenue(df)
    best_product = top_products(df)
    sale_daily = daily_sales(df)
    moving = moving_average(7,2)
    product = db.get_or_404(Product, 2)

    if product.inventory.quantity < moving['predicted_quantity'].iloc[-1]:
        print(f"restock this dude by like atleast{moving['predicted_quantity'].iloc[-1] - product.inventory.quantity}")#TODO: replace print with dict key on the product
    return {
        "total_sold": total_sold,
        "total_sale": total_sale,
        "best_product": best_product.to_dict(),
        "sale_daily": sale_daily,
        "ma": moving.to_dict()
    }

#test routes

@bp.route("/productsdigi",methods=['GET','POST'])
def get_product_json():
    query_category = request.args.get("category")
    if query_category:
        product = db.session.execute(db.select(Product).where(Product.category == query_category)).scalar()
        if not product:
            return jsonify({"error": "Product not found"})
        else:
            return jsonify(product_convertible(product))
    else:
        return jsonify({"error": "Category not found"})

