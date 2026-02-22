from flask import Blueprint,jsonify
from models import Forecast,Product
from schemas import forecasts_schema
from flask_jwt_extended import jwt_required,get_jwt_identity
from analytics import load_sales_df, total_revenue, total_units_sold, top_products, daily_sales, moving_average
from extensions import db

forecasts_bp = Blueprint('forecasts',__name__)

def update_forecast(product_id,mtd='add'):
    forecast = moving_average(window=7, product_id=product_id)
    if forecast is None:
        raise ValueError("Not enough sales data")
    if mtd=='add':
        for i in range(0, forecast.index.max() + 1):
            new_fc = Forecast(
                product_id=product_id,
                date=forecast.date.iloc[i],
                predicted_quantity=forecast.predicted_quantity.iloc[i],
            )
            db.session.add(new_fc)
        db.session.commit()
    elif mtd=='update':
        old_forecasts = db.session.execute(db.select(Forecast)).scalars().all()
        for i,f in enumerate(old_forecasts):
            f.date = forecast.date.iloc[i]
            f.predicted_quantity = forecast.predicted_quantity.iloc[i]
            db.session.add(f)
        db.session.commit()


    elif mtd=='delete':
        all_forecast = db.session.execute(db.select(Forecast)).scalars().all()
        for forecast in all_forecast:
            db.session.delete(forecast)
        db.session.commit()
    else:
        pass



def get_forecast(user_id:int,product_id:int):
    target_forecast = Forecast.query.where(Forecast.product).where(Product.user_id == user_id).order_by(
        Forecast.id.desc()).all()
    if not target_forecast:
        try:
            update_forecast(product_id=product_id, mtd='add')
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
    else:
        try:
            update_forecast(product_id=product_id, mtd='update')
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
    forecast = Forecast.query.where(Forecast.product).where(Product.user_id == user_id).order_by(
        Forecast.id.desc()).all()
    return jsonify(forecasts_schema.dump(forecast))

def get_basic_dashboard(user_id:int):
    df = load_sales_df()
    total_sold = total_units_sold(df)
    total_sale = total_revenue(df)
    best_product = top_products(df)
    sale_daily = daily_sales(df)
    return jsonify({
        "total_item_sold": total_sold,
        "total_revenue": total_sale,
        "best_product": best_product.to_dict(),
        "sale_daily": sale_daily
    }
    )
