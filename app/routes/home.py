# app/routes/home.py
from flask import Blueprint, render_template

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def home():
    # Logic for handling the home page
    return render_template('home.html')