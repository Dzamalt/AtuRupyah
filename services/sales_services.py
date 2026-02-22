from flask import Blueprint,request,jsonify
from models import Sale, Product
from schemas import sale_schema,sales_schema
from extensions import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from services.inventory_services import remove_stock

def create_sale(product_id: int, quantity: int, sale_date: date):

    product = db.session.get(Product, product_id)

    if not product:
        raise ValueError("Product not found")

    remove_stock(product_id, quantity)

    sale = Sale(
        product_id=product_id,
        quantity_sold=quantity,
        sale_date=sale_date,
        price_at_sale=product.price
    )

    db.session.add(sale)
    db.session.commit()

    return sale

def get_sales_history(user_id:int):
    sales = Sale.query.where(Sale.product).where(Product.user_id == user_id).order_by(Sale.id.desc()).all()
    return jsonify(sales_schema.dump(sales)),200

def get_product_sales(user_id:int, product_id:int):
    sales = Sale.query.where(Sale.product).where(Product.user_id == user_id).where(Sale.product_id == product_id).all()
    return jsonify(sales_schema.dump(sales)),200

def create_product_sales(user_id:int, product_id:int,data:dict):
    product = Product.query.where(Product.user_id == user_id).order_by(Product.id.desc()).where(
        Product.id == product_id).first()
    if not product:
        return jsonify({'message': 'No product found'}), 404
    try:
        sales = create_sale(product_id=product_id, quantity=data['quantity'], sale_date=datetime.now())
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    return jsonify(sale_schema.dump(sales)), 200
