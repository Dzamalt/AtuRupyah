from datetime import date

from extensions import db
from models import Product, Inventory, Sale, Forecast
from analytics import moving_average

def inventory_convertible(inventory):
    return {
        "id": inventory.id,
        "product_id": inventory.product_id,
        "quantity": inventory.quantity,
        "reorder_level": inventory.reorder_level
    }

def sale_convertible(sale):
    if not sale:
        return None
    result = []
    for s in sale:
        result.append(
            {
                "id": s.id,
                "product_id": s.product_id,
                "quantity_sold": s.quantity_sold,
                "sale_date": s.sale_date,
                "price_at_sale": s.price_at_sale,
            }
        )
    return result

def product_convertible(item, include_inventory= False,include_sale = False):
    result = {
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'price': float(item.price),
    }
    if include_inventory:
        result['inventory'] = inventory_convertible(item.inventory) if item.inventory else None
    if include_sale:
        result['sale'] = sale_convertible(item.sales)
    return result

def add_stock(product_id: int, amount: int):

    inventory = db.session.execute(
        db.select(Inventory)
        .where(Inventory.product_id == product_id)
    ).scalar_one_or_none()

    if not inventory:
        raise ValueError("Inventory not found")

    if amount <= 0:
        raise ValueError("Invalid amount")

    inventory.quantity += amount
    db.session.commit()


def remove_stock(product_id: int, amount: int):

    inventory = db.session.execute(
        db.select(Inventory)
        .where(Inventory.product_id == product_id)
    ).scalar_one_or_none()

    if not inventory:
        raise ValueError("Inventory not found")

    if inventory.quantity < amount:
        raise ValueError("Not enough stock")

    inventory.quantity -= amount
    db.session.commit()


def create_sale(product_id: int, quantity: int, sale_date: date):

    product = db.session.get(Product, product_id)

    if not product:
        raise ValueError("Product not found")

    remove_stock(product_id, quantity)

    sale = Sale(
        product_id=product_id,
        quantity_sold=quantity,
        sale_date=sale_date,
        price_at_sale=product.price
    )

    db.session.add(sale)
    db.session.commit()

    return sale

#TOD: duplicate detection system if userid is same.
def create_product(user_id,name: str, category: str, price: float,initial_quantity: int,reorder_level: int):
    if not reorder_level:
        reorder_level = 0
    product = Product(
        user_id=user_id,
        name=name,
        category=category,
        price=price
    )
    db.session.add(product)
    db.session.commit()
    inventory = Inventory(
        product_id=product.id,
        quantity=initial_quantity,
        reorder_level=reorder_level
    )
    db.session.add(inventory)
    db.session.commit()
    return product

def is_low_stock(product_id: int) -> bool:
    inventory = db.session.execute(
        db.select(Inventory).where(Inventory.product_id == product_id)
    ).scalar_one_or_none()

    if not inventory:
        return False

    return inventory.quantity <= inventory.reorder_level

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