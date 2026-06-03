from flask import Blueprint, request, render_template, redirect

default_bp = Blueprint("default", __name__)

@default_bp.route("/")
def index():
    return render_template("wiki.html")
@default_bp.route("/wiki")
def wiki():
    return redirect("https://github.com/Dzamalt/AtuRupyah/wiki/AtuRupyah-API-Documentation")


