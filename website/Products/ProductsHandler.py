from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json
from ..ExternalAPI.EndpointAPI import EndpointBuilder, EndpointURLs
from ..ExternalAPI.APIHandller import CallAPI

products = Blueprint("products", __name__)


@products.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        flash("Note added!", category="success")
    else:
        urlreq = EndpointBuilder().BuildURL(EndpointURLs.PRODUCTS_SELLER)

        reqjson = {"SellerId": current_user.get_id()}

        try:
            response = CallAPI(
                "GET",
                urlreq,
                require_authorization=True,
                request_token=current_user.token,
                request_data=reqjson,
            )
            print(response)
            page = {}
            page["home"] = False
            page["products"] = True
            page["orders"] = False

            content = {
                "page": page,
                "user": current_user,
                "inside_content_title": "Products",
                "products_list": response,
            }
            return render_template("Products/ProductsTable.html", model=content)
        except Exception as e:
            print(e)
            raise


@products.route("/edit_product/<product>", methods=["GET"])
@login_required
def edit_product(product):
    if request.method == "GET":
        page = {}
        page["home"] = False
        page["products"] = True
        page["orders"] = False

        content = {
            "page": page,
            "user": current_user,
            "inside_content_title": "Products",
            "product": product,
        }

        print(content)
        return render_template("Products/EditProduct.html", model=content)
    else:
        None


@products.route("/edit_product_status", methods=["POST"])
@login_required
def edit_product_status(product):
    print(product)
    return render_template("Products/EditProduct.html", user=current_user)
