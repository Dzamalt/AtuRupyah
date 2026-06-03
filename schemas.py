from flask_marshmallow import Marshmallow
from models import Product, Inventory, Sale, Forecast

ma = Marshmallow()

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True


class SaleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sale
        load_instance = True


class ForecastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Forecast
        load_instance = True


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

sale_schema = SaleSchema()
sales_schema = SaleSchema(many=True)

forecast_schema = ForecastSchema()
forecasts_schema = ForecastSchema(many=True)