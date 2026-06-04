from flask import Blueprint, request, render_template, redirect

default_bp = Blueprint("default", __name__)

@default_bp.route("/")
def index():
    return render_template("index.html")
@default_bp.route("/wiki")
def wiki():
    return render_template("wiki.html")


