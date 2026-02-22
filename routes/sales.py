from flask import Blueprint,request,jsonify
from models import Sale, Product
from schemas import sale_schema,sales_schema
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.sales_services import get_sales_history, get_product_sales,create_product_sales

sales_bp = Blueprint('sales',__name__)

@sales_bp.route('/')
@jwt_required()
def get_sales_history_route():
    return get_sales_history(user_id=get_jwt_identity())
@sales_bp.route('/<int:p_id>',methods=['GET'])
@jwt_required()
def get_product_sales_route(p_id):
    return get_product_sales(user_id=get_jwt_identity(),product_id=p_id)

@sales_bp.route('/<int:p_id>',methods=['POST'])
@jwt_required()
def create_sales_route(p_id):
    return create_product_sales(user_id=get_jwt_identity(),product_id=p_id,data=request.get_json())
