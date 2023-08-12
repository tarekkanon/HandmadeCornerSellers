from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..ExternalAPI.EndpointAPI import EndpointBuilder, EndpointURLs
from ..ExternalAPI.APIHandller import CallAPI

orders = Blueprint("orders", __name__)


@orders.route("/orders", methods=["GET", "POST"])
@login_required
def seller_orders():
    if request.method == "POST":
        flash("Note added!", category="success")
    else:
        urlreq = EndpointBuilder().BuildURL(EndpointURLs.ORDERS)

        print(urlreq)

        reqjson = {"type": "seller", "SellerId": current_user.get_id()}

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
            page["products"] = False
            page["orders"] = True

            content = {
                "page": page,
                "user": current_user,
                "inside_content_title": "Orders",
                "orders_list": response,
            }

            return render_template("Orders/OrdersTable.html", model=content)
        except Exception as e:
            print(e)
            raise


@orders.route("/order_line_details/<order_line_edit>", methods=["GET"])
@login_required
def order_line_details(order_line_edit):
    if request.method == "GET":
        urlreq = EndpointBuilder().BuildURL(EndpointURLs.ORDERS_LINE)

        reqjson = {"OrderLineId": order_line_edit}

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
            page["products"] = False
            page["orders"] = True

            content = {
                "page": page,
                "user": current_user,
                "inside_content_title": "Orders "
                + str(response[0]["OrderId"])
                + " Customer "
                + response[0]["CustomerName"],
                "order": response[0],
            }

            return render_template("Orders/OrderDetails.html", model=content)
        except Exception as e:
            print(e)
            raise


@orders.route("/update_order", methods=["POST"])
@login_required
def seller_update_order():
    if request.method == "POST":
        if request.form["RequestedOperation"] == "ConfirmOrder":
            urlreq = EndpointBuilder().BuildURL(EndpointURLs.ORDERS_UPDATE_CONFIRM)
        elif request.form["RequestedOperation"] == "CancelOrder":
            urlreq = EndpointBuilder().BuildURL(EndpointURLs.ORDERS_UPDATE_CANCEL)
        else:
            return

        data = {}
        data["OrderId"] = request.form["OrderId"]

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
                url_for(
                    "orders.order_line_details",
                    order_line_edit=request.form["OrderLineId"],
                )
            )
        except Exception as e:
            print(e)
            raise
