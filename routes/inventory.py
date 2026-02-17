from flask import Blueprint,request,jsonify
from models import Inventory
from extensions import db
from schemas import inventory_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from services import add_stock

inventory_bp = Blueprint('inventory',__name__)

@inventory_bp.route('/',methods=['GET'])
@jwt_required()
def index():
    return jsonify({"error": "Missing fields"}), 400

@inventory_bp.route('/<int:p_id>',methods=['GET'])
@jwt_required()
def inventory(p_id):
    user_id = get_jwt_identity()
    target_inventory = Inventory.query.where(Inventory.id == p_id).one_or_none()

    if target_inventory.product.user_id != int(user_id) or not target_inventory:
        return jsonify({'message': 'Inventory not found'}),404
    return jsonify(inventory_schema.dump(target_inventory)),200

@inventory_bp.route('/<int:p_id>',methods=['PUT'])
@jwt_required()
def update_inventory(p_id):
    user_id = get_jwt_identity()
    target_inventory = Inventory.query.where(Inventory.id == p_id).one_or_none()
    data = request.get_json()
    if target_inventory.product.user_id != int(user_id) or not target_inventory:
        return jsonify({'message': 'Inventory not found'}),404
    target_inventory.quantity = data['quantity']
    target_inventory.reorder_level = data['reorder_level']
    db.session.add(target_inventory)
    db.session.commit()
    return jsonify(inventory_schema.dump(target_inventory)),200

@inventory_bp.route('/<int:p_id>',methods=['PUT'])
@jwt_required()
def add_stock(p_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    target_inventory = Inventory.query.where(Inventory.id == p_id).one_or_none()
    if target_inventory.product.user_id != int(user_id) or not target_inventory:
        return jsonify({'message': 'Inventory not found'}),404
    try:
        add_stock(target_inventory, data['quantity'])
    except ValueError as e:
        return jsonify({'message': str(e)}),400
    return jsonify(inventory_schema.dump(target_inventory)),200
