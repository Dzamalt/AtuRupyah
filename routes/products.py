import sqlite3

import sqlalchemy
from flask import Blueprint,request,jsonify
from models import Product
from extensions import db
from schemas import products_schema,product_schema
from services import create_product
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy.exc import IntegrityError

products_bp = Blueprint('products',__name__)

@products_bp.route('/',methods=['GET'])
@jwt_required()
def get_all_products():
    user_id = get_jwt_identity()
    products = Product.query.where(Product.user_id==user_id).order_by(Product.id.desc()).all()
    return jsonify(products_schema.dump(products)),200

@products_bp.route('/<int:p_id>',methods=['GET'])
@jwt_required()
def get_one_product(p_id):
    user_id = get_jwt_identity()
    product = Product.query.where(Product.user_id==user_id).order_by(Product.id.desc()).where(Product.id == p_id).first()
    print(product.sales)
    if not product:
        return jsonify({"message": "Product not found"}),404
    return jsonify(product_schema.dump(product)),200

@products_bp.route('/',methods=['POST'])
@jwt_required()
def manifest_product():
    user_id = get_jwt_identity()
    data = request.get_json()
    if data.get('name') is None or data.get('price') is None or data.get('category') is None or data.get('quantity') is None:
        return jsonify({"message": "Missing fields"}),400
    new_product = create_product(
        user_id=user_id,
        name=data.get('name'),
        price=data.get('price'),
        category=data.get('category'),
        initial_quantity=data.get('quantity'),
        reorder_level=data.get('reorder_level'))
    return jsonify(product_schema.dump(new_product)),201

@products_bp.route('/<int:p_id>',methods=['PUT'])
@jwt_required()
def update_product(p_id):
    user_id = get_jwt_identity()
    product = Product.query.where(Product.user_id==user_id).order_by(Product.id.desc()).where(Product.id == p_id).first()
    if not product:
        return jsonify({"message": "Product not found"}),404
    data = request.get_json()
    product.name = data.get('name',product.name)
    product.price = data.get('price',product.price)
    product.category = data.get('category',product.category)

    db.session.commit()
    return jsonify(product_schema.dump(product)),200

@products_bp.route('/<int:p_id>',methods=['DELETE'])
@jwt_required()
def delete_product(p_id):
    user_id = get_jwt_identity()
    product = Product.query.where(Product.user_id==user_id).order_by(Product.id.desc()).where(Product.id == p_id).first()
    if not product:
        return jsonify({"message": "Product not found"}),404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"}),204