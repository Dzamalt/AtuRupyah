from flask import Blueprint,request,jsonify
from models import Inventory,Product
from extensions import db
from schemas import inventory_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

def grab_inventory(user_id:int,product_id:int):
    return Inventory.query.where(Inventory.product).where(Product.user_id == user_id).where(Inventory.product_id == product_id).one_or_none()

def add_stock(product_id: int,user_id:int, amount: int):

    inventory = grab_inventory(product_id=product_id,user_id=user_id)

    if amount <= 0:
        raise ValueError("Invalid amount")

    inventory.quantity += amount
    db.session.commit()

def remove_stock(product_id: int, amount: int):

    if amount <= 0:
        raise ValueError("Invalid amount")
    inventory = db.session.execute(
        db.select(Inventory)
        .where(Inventory.product_id == product_id)
    ).scalar_one_or_none()

    if inventory.quantity < amount:
        raise ValueError("Not enough stock")

    inventory.quantity -= amount
    db.session.commit()

def get_inventory(user_id:int,product_id:int):
    target_inventory = grab_inventory(user_id=user_id,product_id=product_id)
    if not target_inventory:
        return jsonify({'message': 'Inventory not found'}), 404

    return jsonify(inventory_schema.dump(target_inventory)), 200

def update_inventory(user_id:int,product_id:int,data:dict):
    target_inventory = grab_inventory(user_id=user_id,product_id=product_id)
    if not target_inventory:
        return jsonify({'message': 'Inventory not found'}), 404
    new_re = data.get('new_re')
    if not new_re:
        new_re = target_inventory.reorder_level
    target_inventory.quantity = data['quantity']
    target_inventory.reorder_level = new_re
    db.session.add(target_inventory)
    db.session.commit()
    return jsonify(inventory_schema.dump(target_inventory)), 200

def restock_inventory(user_id:int,product_id:int,data:dict):
    target_inventory = grab_inventory(user_id=user_id,product_id=product_id)
    if not target_inventory:
        return jsonify({'message': 'Inventory not found'}), 404
    try:
        add_stock(product_id=product_id,amount=data['quantity'],user_id=user_id)
    except ValueError as e:
        return jsonify({'message': "Invalid Amount"}), 400
    return jsonify(inventory_schema.dump(target_inventory)), 200