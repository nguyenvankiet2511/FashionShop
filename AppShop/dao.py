from sqlalchemy import func, extract, case
from sqlalchemy.orm import aliased
import google.auth.transport.requests
from pip._vendor import cachecontrol
import requests, os
from flask import request, session, jsonify
from google.oauth2 import id_token
from AppShop import db, flow
from AppShop.models import Categories, Products, Accounts, Users, Carts, Customers, Orders, Shippers, BillingAddress, \
    OrderDetails
import hashlib, datetime


def get_user_oauth():
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    user_oauth = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=os.getenv("642815659525-7hq61q6ueb21ujri2jqnroiomf74pola.apps.googleusercontent.com")
    )
    return user_oauth


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Accounts.query.filter(Accounts.username.__eq__(username.strip()), Accounts.password.__eq__(password)).first()


# Categories------------------------------------->
def get_all_categories():
    return Categories.query.all()


def get_category(id):
    return Categories.query.filter(Categories.id.__eq__(id)).first()


# Products---------------------------------------->
def get_all_products():
    return Products.query.all()


def get_product_limit(limit):
    return Products.query.limit(limit).all()


def get_product_by_caterory_all(category_id):
    if category_id:
        products = Products.query.filter(Products.category_id.__eq__(category_id))
    else:
        products = Products.query.all()
    return products


def get_products_bestSeller(limit):
    return Products.query.order_by(Products.discount.desc()).limit(limit).all()


def get_products_by_category(category_id, limit):
    if category_id:
        products = Products.query.filter(Products.category_id.__eq__(category_id))
    else:
        products = Products.query.all()
    return products[:limit]


def get_product(id):
    return Products.query.filter(Products.id.__eq__(id)).first()


def get_price_product(product_id):
    product = Products.query.filter_by(id=product_id).first()
    if product:
        discounted_price = product.price * (1 - product.discount / 100)
        return discounted_price
    return 0


# Carts-------------------------------------------->
def get_count_cart(user_id):
    return Carts.query.filter(Carts.customer_id == user_id).count()


def get_idProducts_to_cart(user_id):
    return Carts.query.filter(Carts.customer_id.__eq__(user_id)).all()


def get_products_to_cart(user_id):
    return db.session.query(
        Products.id.label('product_id'),
        Products.name.label('product_name'),
        Products.description.label('product_description'),
        Products.imageProduct.label('product_images'),
        Products.discount.label('product_discount'),
        Products.price.label('product_price'),
        Carts.quantity,
        Carts.id.label('cart_id')
    ).join(Carts, Products.id == Carts.product_id) \
        .filter(Carts.customer_id == user_id) \
        .all()


def get_cart_by_id(id):
    return Carts.query.filter(Carts.id == id).first()


def add_to_cart(user_id, product_id, quantity):
    existing_cart_item = Carts.query.filter_by(customer_id=user_id, product_id=product_id).first()
    if existing_cart_item:
        existing_cart_item.quantity += quantity
        db.session.commit()
    else:
        new_cart_item = Carts(customer_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)
        db.session.commit()


def remove_product_to_cart(id):
    # Tìm sản phẩm trong giỏ hàng dựa trên id
    cart = Carts.query.filter(Carts.id == id).first()

    # Nếu sản phẩm tồn tại trong giỏ hàng, thì xóa nó
    if cart:
        db.session.delete(cart)
        db.session.commit()
        print(f"Sản phẩm với ID {id} đã được xóa khỏi giỏ hàng.")
    else:
        print(f"Sản phẩm với ID {id} không tồn tại trong giỏ hàng.")


# Users------------------------------------------->
def get_inf_user(id):
    return Users.query.filter(Users.id.__eq__(id)).first()


def update_quantity_cart(cart_id, new_quantity):
    cart_item = Carts.query.filter_by(id=cart_id).first()
    if cart_item:
        cart_item.quantity = new_quantity
        db.session.commit()


def add_account(fullName, username, password, email):
    # Tạo đối tượng Users
    user = Users(name=fullName, email=email)
    db.session.add(user)
    db.session.commit()  # Commit để có ID cho user

    # Tạo đối tượng Customers với user_id
    customer = Customers(id=user.id)  # user.id đã được gán bởi commit trước đó
    db.session.add(customer)

    # Tạo đối tượng Accounts với user_id
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    account = Accounts(name=fullName, username=username, password=hashed_password, email=email, user_id=user.id)
    db.session.add(account)
    db.session.commit()


# Order----------------------------------------------------------------------
def get_all_orders():
    orders = db.session.query(
        Orders.id,
        Users.name.label('user_name'),
        BillingAddress.address.label('billing_address'),
        Orders.paymentMethods,
        Orders.orderDate,
        Orders.active,
        Orders.totalAmount
    ).join(Users, Orders.customer_id == Users.id) \
        .join(BillingAddress, Orders.billingAddress_id == BillingAddress.id) \
        .filter(Orders.active == False) \
        .all()

    return orders


def get_all_orders_confirm():
    shippers_alias = aliased(Shippers)
    billing_address_alias = aliased(BillingAddress)

    orders = db.session.query(
        Orders.id,
        Users.name.label('user_name'),
        billing_address_alias.address.label('billing_address'),
        Orders.paymentMethods,
        Orders.orderDate,
        Orders.active,
        Orders.totalAmount
    ).join(Users, Orders.customer_id == Users.id) \
        .outerjoin(shippers_alias, Orders.shipper_id == shippers_alias.id) \
        .outerjoin(billing_address_alias, Orders.billingAddress_id == billing_address_alias.id) \
        .filter(Orders.active == True) \
        .all()

    return orders


def get_orders_by_id(order_id):
    # Tạo alias cho bảng Users
    orders = db.session.query(
        Orders.id,
        Users.name.label('customer_name'),  # Giả định rằng đây là tên khách hàng
        BillingAddress.address.label('billing_address'),
        BillingAddress.phone.label('phone'),
        Orders.paymentMethods,
        Orders.orderDate,
        Orders.active,
        Orders.totalAmount
    ).join(Users, Orders.customer_id == Users.id) \
        .join(BillingAddress, Orders.billingAddress_id == BillingAddress.id) \
        .filter(Orders.id == order_id) \
        .first()  # Dùng .first() để lấy một kết quả duy nhất
    return orders


def get_order_details_with_info():
    # Truy vấn để lấy các thuộc tính cần thiết từ các bảng liên quan
    results = (
        db.session.query(
            OrderDetails.id.label("order_detail_id"),
            Products.name.label("product_name"),
            OrderDetails.product_id.label("product_id"),
            OrderDetails.quantity.label("quantity"),
            OrderDetails.price.label("price"),
            Orders.orderDate.label("order_time"),
            Users.name.label("customer_name"),
            Orders.active.label("status")
        )
        .join(Products, Products.id == OrderDetails.product_id)
        .join(Orders, Orders.id == OrderDetails.order_id)
        .join(Customers, Customers.id == Orders.customer_id)
        .join(Users, Users.id == Customers.id)
        .all()
    )

    return results


def chang_active_order(order_id):
    # Find the order by ID
    order = db.session.query(Orders).filter_by(id=order_id).first()

    if order:
        order.active = not order.active
        db.session.commit()
        return f"Order {order_id} active status changed to {order.active}."
    else:
        return f"Order {order_id} not found."


def chang_active_order_list(order_id):
    for i in range(len(order_id)):
        id = order_id[i]
        order = db.session.query(Orders).filter_by(id=id).first()
        if order:
            order.active = not order.active
            db.session.commit()
            return f"Order {order_id} active status changed to {order.active}."
        else:
            return f"Order {order_id} not found."


from decimal import Decimal
from datetime import datetime

from decimal import Decimal


def create_order(name, phone, ngaySinh, diaChi, employee_id, l_productId, l_soLuong):
    # Tạo người dùng và khách hàng
    user = Users(name=name, phone=phone, address=diaChi, birthDate=ngaySinh)
    db.session.add(user)
    db.session.flush()  # Đảm bảo user được thêm vào để có thể dùng id của nó ngay lập tức

    customer = Customers(id=user.id)  # Giả sử có quan hệ qua user_id
    db.session.add(customer)
    db.session.flush()  # Đảm bảo customer được thêm vào trước khi tạo đơn hàng

    # Tính tổng tiền đơn hàng
    totals = 0
    for i in range(len(l_productId)):
        price = get_price_product(l_productId[i])
        if price is None or price == '':
            raise ValueError(f"Không tìm thấy giá cho sản phẩm với ID {l_productId[i]}")
        try:
            price = float(price)  # Đảm bảo giá là số thực
        except ValueError:
            raise ValueError(f"Giá sản phẩm với ID {l_productId[i]} không hợp lệ")

        quantity = l_soLuong[i]
        if quantity is None or quantity == '':
            raise ValueError(f"Số lượng cho sản phẩm với ID {l_productId[i]} không hợp lệ")
        try:
            quantity = int(quantity)  # Đảm bảo số lượng là số nguyên
        except ValueError:
            raise ValueError(f"Số lượng cho sản phẩm với ID {l_productId[i]} không hợp lệ")

        totals += price * quantity

    # Tạo đơn hàng
    order = Orders(customer_id=customer.id, employee_id=employee_id, orderDate=datetime.now().date(), active=True,
                   totalAmount=totals)
    db.session.add(order)
    db.session.flush()

    # Tạo chi tiết đơn hàng
    for i in range(len(l_productId)):
        product = get_product(l_productId[i])
        if product is None:
            raise ValueError(f"Không tìm thấy sản phẩm với ID {l_productId[i]}")

        quantity = l_soLuong[i]
        try:
            quantity = int(quantity)  # Đảm bảo số lượng là số nguyên
        except ValueError:
            raise ValueError(f"Số lượng cho sản phẩm với ID {l_productId[i]} không hợp lệ")

        order_detail = OrderDetails(
            product_id=l_productId[i],
            quantity=quantity,
            price=product.price,
            discount=product.discount,
            order_id=order.id
        )
        print(order_detail.id)
        db.session.add(order_detail)

    # Lưu tất cả thay đổi vào cơ sở dữ liệu
    db.session.commit()


def create_order_customer(customer_id, address_id, total, paymentMethods, l_cartId):
    new_order = Orders(customer_id=customer_id, billingAddress_id=address_id,
                       paymentMethods=paymentMethods, totalAmount=total, active=False, )
    db.session.add(new_order)
    for i in range(len(l_cartId)):
        cart = get_cart_by_id(l_cartId[i])
        print(cart.product_id)
        product = Products.query.filter(Products.id == cart.product_id).first()
        if product:
            new_order_detail = OrderDetails(order_id=new_order.id, product_id=product.id, price=product.price,
                                            quantity=cart.quantity, discount=product.discount)
            db.session.add(new_order_detail)
            remove_product_to_cart(l_cartId[i])
        db.session.commit()


# Address--------------------------------------------------------------
def get_address_by_user_id(user_id):
    return BillingAddress.query.filter(BillingAddress.customer_id == user_id).all()


# daonh thu theo năm
def get_revenue_by_year(year):
    # Truy vấn để tính tổng doanh thu của các đơn hàng trong một năm cụ thể
    revenue = (
        db.session.query(func.sum(Orders.totalAmount).label("total_revenue"))
        .filter(extract('year', Orders.orderDate) == year)  # Lọc các đơn hàng theo năm
        .filter(Orders.active == True)  # Chỉ tính các đơn hàng đã được xác nhận
        .scalar()  # Trả về giá trị doanh thu
    )

    return revenue or 0  # Trả về 0 nếu không có doanh thu nào


# số lượng mặt hàng đã bán
def get_total_items_sold_by_year(year):
    total_quantity = (
        db.session.query(func.sum(OrderDetails.quantity).label("total_items_sold"))
        .join(Orders, Orders.id == OrderDetails.order_id)
        .filter(Orders.active == True)
        .filter(extract('year', Orders.orderDate) == year)
        .scalar()
    )

    return total_quantity or 0


# doanh thu theo quý
def get_revenue_by_quarter(year):
    result = []
    for quarter in range(1, 5):
        # Xác định điều kiện cho mỗi quý
        start_month = (quarter - 1) * 3 + 1
        end_month = quarter * 3

        query = (
            db.session.query(
                func.coalesce(func.sum(Orders.totalAmount), 0).label('total_revenue')
            )
            .filter(
                extract('year', Orders.orderDate) == year,
                extract('month', Orders.orderDate) >= start_month,
                extract('month', Orders.orderDate) <= end_month
            )
            .scalar()  # Dùng scalar() để lấy giá trị duy nhất
        )
        result.append(query if query else 0)
    return result

#daoanh thu 4 nam
def get_revenue_last_4_years():
    # Lấy năm hiện tại
    current_year = datetime.now().year

    # Tạo danh sách các năm gần nhất
    years = [current_year - i for i in range(4)]

    # Truy vấn doanh thu theo năm
    revenue_by_year = (
        db.session.query(
            extract('year', Orders.orderDate).label('year'),
            func.sum(Orders.totalAmount).label('total_revenue')
        )
        .filter(Orders.active == True)  # Chỉ tính các đơn hàng đã xác nhận
        .filter(extract('year', Orders.orderDate).in_(years))  # Lọc theo các năm gần nhất
        .group_by(extract('year', Orders.orderDate))
        .order_by(extract('year', Orders.orderDate).desc())  # Sắp xếp theo năm giảm dần
        .all()
    )

    # Định dạng kết quả
    result = {year: 0 for year in years}
    for year, total_revenue in revenue_by_year:
        result[year] = total_revenue

    return result
