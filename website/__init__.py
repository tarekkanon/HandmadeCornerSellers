from flask import Flask, render_template
from flask_login import LoginManager
import urllib.request as ureq, json
from website.Auth import SellerModel
from .ExternalAPI.EndpointAPI import EndpointBuilder, EndpointURLs
from .ExternalAPI.APIHandller import CallAPI


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "randomsecretphrase"

    from .Products.ProductsHandler import products
    from .Auth.auth import auth

    app.register_blueprint(products, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    

    @login_manager.user_loader
    def load_user(seller_id):
        urlreq = EndpointBuilder().BuildURL(EndpointURLs.SELLERS_LOGIN_SESSION)

        reqjson = {
                "SellerId" : seller_id
            }

        try:
            seller = SellerModel.Seller(CallAPI(call_method='POST', request_url=urlreq, require_authorization = False, request_data= reqjson)[0])

            return seller
        except Exception as e:
            print(e)
        
        return None

    return app


