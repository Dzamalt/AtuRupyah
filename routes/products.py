from flask import Blueprint,request,jsonify
from models import Product
from extensions import db
from schemas import products_schema,product_schema
from flask_jwt_extended import jwt_required,get_jwt_identity
from services.products_services import get_products, get_product_by_id,create_new_product,update_product,delete_product

products_bp = Blueprint('products',__name__)

@products_bp.route('/',methods=['GET'])
@jwt_required()
def get_all_products_route():
    """
    get all products from users database
    :return:
    {
    "products": [
    TBA]
    }
    """

    return jsonify(products_schema.dump(get_products(get_jwt_identity()))),200

@products_bp.route('/<int:p_id>',methods=['GET'])
@jwt_required()
def get_one_product_route(p_id):
    """
    get one product from users database
    :param p_id:
    :return:
    """
    return get_product_by_id(user_id=get_jwt_identity(),product_id=p_id)
@products_bp.route('/',methods=['POST'])
@jwt_required()
def create_product_route():
    """
    create new product
    :return:
    """
    return create_new_product(get_jwt_identity(), request.get_json())


@products_bp.route('/<int:p_id>',methods=['PUT'])
@jwt_required()
def update_product_route(p_id):
    """
    update product
    :param p_id:
    :return:
    """
    return update_product(user_id=get_jwt_identity(),product_id=p_id,data=request.get_json())

@products_bp.route('/<int:p_id>',methods=['DELETE'])
@jwt_required()
def delete_product_route(p_id):
    """
    delete product
    :param p_id:
    :return:
    """
    return delete_product(user_id=get_jwt_identity(),product_id=p_id)
