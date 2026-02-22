import logging

from flask import jsonify
from models import Product, Inventory
from schemas import product_schema
from extensions import db

def get_products(user_id:int):
    return Product.query.where(Product.user_id == user_id).order_by(Product.id.desc()).all()

def get_product_by_id(user_id:int,product_id:int):
    product = Product.query.where(Product.user_id == user_id).order_by(Product.id.desc()).where(
        Product.id == product_id).first()
    if product is None:
        return jsonify({"message": "Product not found"}), 404
    return product_schema.dump(product), 200

def create_new_product(user_id:int, data: dict):
    if not data.get('reorder_level'):
        reorder_level = 0
    else:
        reorder_level = int(data.get('reorder_level'))
    if data.get('name') is None or data.get('price') is None or data.get('category') is None or data.get('quantity') is None:
        logging.error("missing required fields")
        return jsonify({"message": "Missing fields"}), 400
    product = Product(
        user_id=user_id,
        name=data.get('name'),
        category=data.get('category'),
        price=data.get('price')
    )
    db.session.add(product)
    db.session.commit()
    inventory = Inventory(
        product_id=product.id,
        quantity=data.get('quantity'),
        reorder_level=reorder_level
    )
    db.session.add(inventory)
    db.session.commit()
    return product_schema.dump(product), 201

def update_product(user_id:int, product_id:int, data: dict):
    product = Product.query.where(Product.user_id==user_id).order_by(Product.id.desc()).where(Product.id == product_id).first()
    if not product:
        return jsonify({"message": "Product not found"}),404
    product.name = data.get('name',product.name)
    product.price = data.get('price',product.price)
    product.category = data.get('category',product.category)

    db.session.commit()
    return product_schema.dump(product),200

def delete_product(user_id:int, product_id:int):
    product = Product.query.where(Product.user_id == user_id).order_by(Product.id.desc()).where(
        Product.id == product_id).first()
    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 204