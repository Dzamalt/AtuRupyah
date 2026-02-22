from flask import Blueprint, request
import logging
from services.auth_services import register_user,login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    reg = register_user(request.get_json())
    return reg if reg else logging.error("register error")
@auth_bp.route("/login", methods=["POST"])
def login():
    log = login_user(request.get_json())
    return log if log else logging.error("register error")
