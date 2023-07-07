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
        except Exception as e:
            print(e)
            raise

    return render_template("Products/ProductsTable.html", model=content)
