import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from extensions import db
from models import Sale,Product


def load_sales_df():
    query = db.session.query(
        Sale.id,
        Sale.sale_date,
        Sale.product_id,
        Sale.quantity_sold,
        Sale.price_at_sale,
        Product.name.label("product_name"),
    ).join(Product, Sale.product_id == Product.id)
    result = query.all()

    df = pd.DataFrame(result,columns=[
        "id",
        "date",
        "product_id",
        "quantity",
        "price",
        "product_name",
    ])

    return df

def total_units_sold(df):
    return int(df['quantity'].sum())

def total_revenue(df):
    return float((df["quantity"] * df["price"]).sum())

def top_products(df,limit=5):
    return (
        df.groupby('product_name')["quantity"].sum().sort_values(ascending=False).head(limit)
    )

def daily_sales(df):

    df["date"] = pd.to_datetime(df["date"])

    grouped = (
        df.groupby(df["date"].dt.date)["quantity"]
        .sum()
        .sort_index()
    )

    # Convert date keys to strings
    return {
        str(date): int(qty)
        for date, qty in grouped.items()
    }

def prepare_daily_sales(df, product_id):

    product_df = df[df["product_id"] == product_id].copy()

    # Convert to datetime
    product_df["date"] = pd.to_datetime(
        product_df["date"],
        errors="coerce"
    )

    product_df = product_df.dropna(subset=["date"])

    # Normalize time -> 00:00:00
    product_df["date"] = product_df["date"].dt.normalize()

    # Aggregate per day
    daily = (
        product_df
        .groupby("date")["quantity"]
        .sum()
        .sort_index()
    )

    # Create full date range (daily)
    full_range = pd.date_range(
        start=daily.index.min(),
        end=daily.index.max(),
        freq="D"
    )

    # Fill missing days with 0
    daily = daily.reindex(full_range, fill_value=0)

    daily.index.name = "date"
    daily.name = "quantity"

    return daily.reset_index()

def moving_average(window=7, product_id=None):

    df = load_sales_df()
    daily = prepare_daily_sales(df, product_id)

    if daily is None or len(daily) < 5:
        return None

    daily = daily.sort_values("date")

    daily["ma"] = (
        daily["quantity"]
        .rolling(window=window, min_periods=1)
        .mean()
    )

    last_ma = daily["ma"].iloc[-1]

    last_date = daily["date"].iloc[-1]

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=window,
        freq="D"
    )

    forecast = pd.DataFrame({
        "date": future_dates,
        "predicted_quantity": [round(last_ma, 2)] * window
    })

    return forecast