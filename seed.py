import random
from datetime import datetime, timedelta

from app import app
from extensions import db
from models import Product, Inventory, Sale, User


def seed_database():

    with app.app_context():

        # ---- Clear old data (optional) ----
        # db.session.query(Sale).delete()
        # db.session.query(Inventory).delete()
        # db.session.query(Product).delete()
        # db.session.query(User).delete()
        # db.session.commit()

        # ---- Create test user ----

        # ---- Sample products ----
        products_data = [
            ("Laptop", "Electronics", 1200),
            ("Mouse", "Electronics", 25),
            ("Keyboard", "Electronics", 80),
            ("Monitor", "Electronics", 300),
            ("Desk", "Furniture", 400),
            ("Chair", "Furniture", 200),
            ("Lamp", "Furniture", 60),
            ("Notebook", "Stationery", 5),
            ("Pen", "Stationery", 2),
            ("Backpack", "Accessories", 70),
        ]

        products = []

        for name, category, price in products_data:

            p = Product(
                user_id=1,
                name=name,
                category=category,
                price=price
            )

            db.session.add(p)
            products.append(p)

        db.session.commit()

        # ---- Inventory ----
        for p in products:

            inv = Inventory(
                product_id=p.id,
                quantity=random.randint(30, 100),
                reorder_level=10
            )

            db.session.add(inv)

        db.session.commit()

        # ---- Sales (last 60 days) ----
        for p in products:

            for _ in range(random.randint(10, 25)):

                days_ago = random.randint(0, 60)

                sale_date = datetime.now() - timedelta(days=days_ago)

                quantity = random.randint(1, 5)

                sale = Sale(
                    product_id=p.id,
                    quantity_sold=quantity,
                    sale_date=sale_date.date(),
                    price_at_sale=p.price
                )

                db.session.add(sale)

        db.session.commit()

        print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()
