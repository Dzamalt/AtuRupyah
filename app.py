from flask import Flask
from dotenv import load_dotenv
from extensions import db
from schemas import ma
from routes.inventory import inventory_bp
from routes.products import products_bp
from routes.sales import sales_bp
from routes.forecasts import forecasts_bp
from routes.auth import auth_bp
from routes.default import default_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
    db.init_app(app)
    ma.init_app(app)

    return app

app = create_app()
CORS(app, origins="*")
jwt = JWTManager(app)
app.register_blueprint(default_bp)
app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(sales_bp, url_prefix='/api/sales')
app.register_blueprint(forecasts_bp, url_prefix='/api/forecasts')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

with app.app_context():
    db.create_all()

