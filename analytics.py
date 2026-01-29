import pandas as pd
import numpy as np
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