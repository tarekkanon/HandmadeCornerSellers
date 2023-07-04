from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import urllib.request as ureq, json
from . import SellerModel
from ..ExternalAPI.EndpointAPI import EndpointBuilder, EndpointURLs
from ..ExternalAPI.APIHandller import CallAPI

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        urlreq = EndpointBuilder().BuildURL(EndpointURLs.SELLERS_LOGIN)

        reqjson = {
                "SellerEmail" : email,
                "SellerPassword" : password
            }

        try:

            response = CallAPI('POST', urlreq, require_authorization=False, request_data = reqjson)
            seller = SellerModel.Seller(response[0])
            flash('Logged in successfully!', category='success')
            login_user(seller, remember=True)
            return redirect(url_for('products.home'))

        except Exception as e:
            print(e)
            flash('Incorrect email or password, try again.', category='error')
    else:
        if current_user.is_authenticated:
            return redirect(url_for('products.home'))

    return render_template("loginv2.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # user = User.query.filter_by(email=email).first()
        if True:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # new_user = User(email=email, first_name=first_name, password=generate_password_hash(
            #     password1, method='sha256'))
            # db.session.add(new_user)
            # db.session.commit()
            login_user("", remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('products.home'))


    return render_template("register.html", user=current_user)