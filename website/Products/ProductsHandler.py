from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json

products = Blueprint('products', __name__)


@products.route('/', methods=['GET', 'POST'])
@login_required
def home():

        page = {}
        page['home'] = False
        page['products'] = True
        page['orders'] = False

        content = {'page' : page , 'user' : current_user, 'inside_content_title' : 'Title test'}


        if request.method == 'POST': 
                flash('Note added!', category='success')

        return render_template("seller_panel.html" , model = content)
