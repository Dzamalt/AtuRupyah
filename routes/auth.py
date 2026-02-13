from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from flask_jwt_extended import (
    create_access_token
)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(username=data.get("username")).first():
        return jsonify({"error": "Username already exists"}), 400
    elif User.query.filter_by(email=data.get("email")).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(
        username=data["username"],
        email=data.get("email")
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data.get("password")):
        return jsonify({"error": "Invalid Credentials"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": token, "token_type": "access"}), 200

