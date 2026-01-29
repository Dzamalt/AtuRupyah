from datetime import date

from extensions import db
from models import Product, Inventory, Sale

def inventory_convertible(inventory):
    return {
        "id": inventory.id,
        "product_id": inventory.product_id,
        "quantity": inventory.quantity,
        "reorder_level": inventory.reorder_level,
    }

def sale_convertible(sale):
    return {
        "id": sale.id,
        "product_id": sale.product_id,
        "quantity_sold": sale.quantity_sold,
        "sale_date": sale.sale_date,
        "price_at_sale": sale.price_at_sale,
    }

def product_convertible(item):
    return {
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'price': float(item.price),
        'inventory': inventory_convertible(item.inventory) if item.inventory else None,
        'sale': [sale_convertible(s) for s in item.sales]
    }

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

def is_low_stock(product_id: int) -> bool:
    inventory = db.session.execute(
        db.select(Inventory).where(Inventory.product_id == product_id)
    ).scalar_one_or_none()

    if not inventory:
        return False

    return inventory.quantity <= inventory.reorder_level