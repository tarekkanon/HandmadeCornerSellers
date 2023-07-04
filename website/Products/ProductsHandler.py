from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json

products = Blueprint('products', __name__)


@products.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
            flash('Note added!', category='success')

    return render_template("seller_panel.html", user=current_user)
