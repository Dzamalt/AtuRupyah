from flask import Blueprint,jsonify
from models import Forecast,Product
from schemas import forecasts_schema
from flask_jwt_extended import jwt_required,get_jwt_identity
from analytics import load_sales_df, total_revenue, total_units_sold, top_products, daily_sales, moving_average,get_low_stock_products
from extensions import db

forecasts_bp = Blueprint('forecasts',__name__)

def update_forecast(product_id: int, user_id: int):
    forecast = moving_average(window=7, product_id=product_id,user_id=user_id)

    if forecast is None:
        return jsonify({"message": "Not enough sales"})

    existing = (
        Forecast.query
        .join(Product)
        .where(Product.user_id == user_id)
        .filter(Forecast.product_id == product_id)
        .order_by(Forecast.id.asc())
        .all()
    )

    if not existing:
        for i in range(len(forecast)):
            new_fc = Forecast(
                product_id=product_id,
                date=forecast["date"].iloc[i].to_pydatetime().date(),
                predicted_quantity=float(forecast["predicted_quantity"].iloc[i]),
            )
            db.session.add(new_fc)
    else:
        for i, f in enumerate(existing):
            if i >= len(forecast):
                break
            f.date = forecast["date"].iloc[i].to_pydatetime().date()
            f.predicted_quantity = float(forecast["predicted_quantity"].iloc[i])

    db.session.commit()

    return jsonify(forecasts_schema.dump(existing))


def update_all_forecasts(user_id:int):
    products = Product.query.where(Product.user_id == user_id).all()
    for product in products:
        update_forecast(user_id=user_id, product_id=product.id)
    product_forecasts = (Forecast.query.where(Forecast.product).where(Product.user_id == user_id)
                         .order_by(Forecast.id.desc()).all())
    return product_forecasts

def get_forecast(user_id:int,product_id:int):
    return update_forecast(product_id=product_id, user_id=user_id)

def get_basic_dashboard(user_id:int):
    df = load_sales_df(user_id)
    total_sold = total_units_sold(df)
    total_sale = total_revenue(df)
    best_product = top_products(df)
    sale_daily = daily_sales(df)
    danger_product = get_low_stock_products(user_id)
    return jsonify({
        "danger_product": danger_product,
        "total_item_sold": total_sold,
        "total_revenue": total_sale,
        "best_product": best_product.to_dict(),
        "sale_daily": sale_daily
    }
    )
