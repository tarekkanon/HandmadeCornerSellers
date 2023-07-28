from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
        urlreq = EndpointBuilder().BuildURL(EndpointURLs.PRODUCTS) + product

        try:
            response = CallAPI(
                "GET",
                urlreq,
                require_authorization=True,
                request_token=current_user.token,
                request_data="",
            )

            page = {}
            page["home"] = False
            page["products"] = True
            page["orders"] = False

            print(response)

            category_list = []
            for item in response["categories"]:
                cat = {}
                # cat["CategoryId"] = item["CategoryId"]
                cat["text"] = item["CategoryName"]
                cat["selectable"] = False
                cat["nodeType"] = "main"

                if cat["text"] not in category_list:
                    sub_category_list = []

                    for subItem in response["categories"]:
                        subCat = {}
                        # subCat["SubCategoryId"] = subItem["SubCategoryId"]
                        subCat["text"] = subItem["SubCategoryName"]
                        subCat["nodeType"] = "sub"
                        sub_category_list.append(subCat)

                    cat["nodes"] = sub_category_list

                    category_list.append(cat)

            print(category_list)

            content = {
                "page": page,
                "user": current_user,
                "inside_content_title": "Product",
                "product": response["product"][0],
                "categories": category_list,
            }

            return render_template("Products/EditProduct.html", model=content)
        except Exception as e:
            print(e)
            raise


@products.route("/edit_product_details", methods=["POST"])
@login_required
def edit_product_details():
    if request.method == "POST":
        if request.form["RequestedOperation"] == "UpdateProductOption":
            print(request.form)
            urlreq = EndpointBuilder().BuildURL(EndpointURLs.PRODUCTS_UPDATE_OPTION)

            data = {}
            data["ProductOptionName"] = request.form["ProductOptionName"]
            data["ProductOptionStatus"] = 0

            if "ProductOptionStatus" in request.form:
                if request.form["ProductOptionStatus"] == "on":
                    data["ProductOptionStatus"] = 1

            data["ProductOptionId"] = request.form["ProductOptionId"]

            try:
                response = CallAPI(
                    "PUT",
                    urlreq,
                    require_authorization=True,
                    request_token=current_user.token,
                    request_data=data,
                )

                print(response)

                return redirect(
                    url_for("products.edit_product", product=request.form["ProductId"])
                )
            except Exception as e:
                print(e)
                raise
        elif request.form["RequestedOperation"] == "UpdateProductVariant":
            print(request.form)
            urlreq = EndpointBuilder().BuildURL(EndpointURLs.PRODUCTS_UPDATE_VARIANT)

            data = {}
            data["ProductVariantName"] = request.form["ProductVariantName"]
            data["ProductVariantPrice"] = request.form["ProductVariantPrice"]
            data["ProductVariantUnit"] = request.form["ProductVariantUnit"]
            data["ProductVariantId"] = request.form["ProductVariantId"]

            try:
                response = CallAPI(
                    "PUT",
                    urlreq,
                    require_authorization=True,
                    request_token=current_user.token,
                    request_data=data,
                )

                print(response)

                return redirect(
                    url_for("products.edit_product", product=request.form["ProductId"])
                )
            except Exception as e:
                print(e)
                raise
        elif request.form["RequestedOperation"] == "UpdateProduct":
            print(request.form)
            urlreq = EndpointBuilder().BuildURL(EndpointURLs.PRODUCTS_UPDATE)

            data = {}
            data["ProductName"] = request.form["ProductName"]
            data["ProductDescription"] = request.form["ProductDescription"]
            data["ProductUnit"] = request.form["ProductUnit"]

            data["ProductStatus"] = 0

            if "ProductStatus" in request.form:
                if request.form["ProductStatus"] == "on":
                    data["ProductStatus"] = 1

            data["ProductId"] = request.form["ProductId"]

            try:
                response = CallAPI(
                    "PUT",
                    urlreq,
                    require_authorization=True,
                    request_token=current_user.token,
                    request_data=data,
                )

                print(response)

                return redirect(
                    url_for("products.edit_product", product=request.form["ProductId"])
                )
            except Exception as e:
                print(e)
                raise
        elif request.form["RequestedOperation"] == "NewProductOption":
            print(request.form)
            urlreq = EndpointBuilder().BuildURL(EndpointURLs.PRODUCTS_NEW_OPTION)

            data = {}

            data["ProductId"] = request.form["ProductId"]
            data["ProductOptionName"] = request.form["ProductOptionName"]
            data["ProductOptionStatus"] = 0

            if "ProductOptionStatus" in request.form:
                if request.form["ProductOptionStatus"] == "on":
                    data["ProductOptionStatus"] = 1

            try:
                response = CallAPI(
                    "POST",
                    urlreq,
                    require_authorization=True,
                    request_token=current_user.token,
                    request_data=data,
                )

                print(response)

                return redirect(
                    url_for("products.edit_product", product=request.form["ProductId"])
                )
            except Exception as e:
                print(e)
                raise
        elif request.form["RequestedOperation"] == "NewProductVariant":
            print(request.form)
            urlreq = EndpointBuilder().BuildURL(EndpointURLs.PRODUCTS_NEW_VARIANT)

            data = {}
            data["ProductId"] = request.form["ProductId"]
            data["ProductOptionId"] = request.form["ProductOptionId"]
            data["ProductVariantName"] = request.form["ProductVariantName"]
            data["ProductVariantPrice"] = request.form["ProductVariantPrice"]
            data["ProductVariantUnit"] = request.form["ProductVariantUnit"]

            try:
                response = CallAPI(
                    "POST",
                    urlreq,
                    require_authorization=True,
                    request_token=current_user.token,
                    request_data=data,
                )

                print(response)

                return redirect(
                    url_for("products.edit_product", product=request.form["ProductId"])
                )
            except Exception as e:
                print(e)
                raise

    return redirect(url_for("products.home"))
