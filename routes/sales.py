from flask import Blueprint,request,jsonify
from models import Sale, Product
from extensions import db
from schemas import sale_schema,sales_schema
from services import create_sale
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

sales_bp = Blueprint('sales',__name__)

@sales_bp.route('/')
@jwt_required()
def get_sales_history():
    user_id = get_jwt_identity()
    sales = Sale.query.where(Sale.product).where(Product.user_id == user_id).order_by(Sale.id.desc()).all()
    return jsonify(sales_schema.dump(sales)),200
@sales_bp.route('/<int:p_id>',methods=['GET'])
@jwt_required()
def get_product_sales(p_id):
    user_id = get_jwt_identity()
    sales = Sale.query.where(Sale.product).where(Product.user_id == user_id).where(Sale.product_id == p_id).all()
    if not sales:
        return jsonify({'message': 'No sales found'}),404
    return jsonify(sales_schema.dump(sales)),200
@sales_bp.route('/<int:p_id>',methods=['POST'])
@jwt_required()
def create_sales(p_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    product = Product.query.where(Product.user_id==user_id).order_by(Product.id.desc()).where(Product.id == p_id).first()
    if not product:
        return jsonify({'message': 'No product found'}),404
    sales = create_sale(product_id=p_id,quantity=data['quantity'],sale_date=datetime.now())
    return jsonify(sale_schema.dump(sales)),200
