from datetime import date, datetime
from typing import List, Optional

from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, event, ForeignKey, Date, Numeric
from sqlalchemy.engine import Engine
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from dotenv import load_dotenv
from forms import LoginForm, RegisterForm
from services import product_convertible, sale_convertible, inventory_convertible
from extensions import db
from routes import bp

load_dotenv()





@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
    db.init_app(app)
    return app

app = create_app()
app.register_blueprint(bp)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"
# ^Uncomment when adding users





# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    app.run(debug=True, port=5002)
