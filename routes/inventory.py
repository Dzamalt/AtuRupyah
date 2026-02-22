from flask import Blueprint,request,jsonify
from models import Inventory
from extensions import db
from schemas import inventory_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.inventory_services import get_inventory,update_inventory,restock_inventory

inventory_bp = Blueprint('inventory',__name__)

@inventory_bp.route('/',methods=['GET'])
@jwt_required()
def index():
    return jsonify({"error": "Missing product id"}), 400

@inventory_bp.route('/<int:p_id>',methods=['GET'])
@jwt_required()
def inventory_route(p_id):
    return get_inventory(user_id=get_jwt_identity(),product_id=p_id)

@inventory_bp.route('/<int:p_id>',methods=['PUT'])
@jwt_required()
def update_inventory_route(p_id):
    return update_inventory(user_id=get_jwt_identity(),product_id=p_id,data=request.get_json())

@inventory_bp.route('/<int:p_id>',methods=['PATCH'])
@jwt_required()
def restock_inventory_route(p_id):
    return restock_inventory(user_id=get_jwt_identity(),product_id=p_id,data=request.get_json())

