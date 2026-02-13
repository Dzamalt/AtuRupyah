from flask import Blueprint,request,jsonify
from models import Forecast,Product
from extensions import db
from schemas import forecasts_schema,forecast_schema
from flask_jwt_extended import jwt_required,get_jwt_identity
from analytics import load_sales_df,total_revenue,total_units_sold,top_products,daily_sales
from services import update_forecast
forecasts_bp = Blueprint('forecasts',__name__)

@forecasts_bp.route('/',methods=['GET'])
@jwt_required()
def index():
    return jsonify({"error": "Missing fields"}), 400

@forecasts_bp.route('/dashboard',methods=['GET'])
@jwt_required()
def get_basic_analysis():
    df = load_sales_df()
    total_sold = total_units_sold(df)
    total_sale = total_revenue(df)
    best_product = top_products(df)
    sale_daily = daily_sales(df)
    print(type(sale_daily))
    return jsonify({
        "total_item_sold": total_sold,
        "total_revenue": total_sale,
        "best_product": best_product.to_dict(),
        "sale_daily": sale_daily
    }
    )

@forecasts_bp.route('/<int:p_id>',methods=['GET'])
@jwt_required()
def get_forecast(p_id):
    user_id = get_jwt_identity()
    target_forecast = Forecast.query.where(Forecast.product).where(Product.user_id == user_id).order_by(Forecast.id.desc()).all()
    if not target_forecast:
        update_forecast(product_id=p_id,mtd='add')
    else:
        update_forecast(product_id=p_id,mtd='update')
    forecast = Forecast.query.where(Forecast.product).where(Product.user_id == user_id).order_by(Forecast.id.desc()).all()
    return jsonify(forecasts_schema.dump(forecast))


