from flask import Blueprint,jsonify
from models import Forecast,Product
from schemas import forecasts_schema
from flask_jwt_extended import jwt_required,get_jwt_identity
from services.forecasts_services import get_forecast,get_basic_dashboard,update_all_forecasts
forecasts_bp = Blueprint('forecasts',__name__)

@forecasts_bp.route('/',methods=['GET'])
@jwt_required()
def index():
    return jsonify({"error": "Missing fields"}), 400

@forecasts_bp.route('/dashboard',methods=['GET'])
@jwt_required()
def get_basic_analysis_route():
    update_all_forecasts(get_jwt_identity())
    return get_basic_dashboard(user_id=get_jwt_identity())

@forecasts_bp.route('/<int:p_id>',methods=['GET'])
@jwt_required()
def get_forecast_route(p_id):
    return get_forecast(user_id=get_jwt_identity(),product_id=p_id)

