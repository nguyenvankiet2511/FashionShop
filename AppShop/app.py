from AppShop import app, dao, login, flow
from AppShop.models import UsersRole, Accounts, Users, Products, Customers
from flask import render_template, session, flash, jsonify, redirect, request, url_for
from flask_login import login_user, current_user, logout_user
from AppShop.admin import *


@app.route("/")
def home():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        countCart = dao.get_count_cart(user_id)
    else:
        user = None
        countCart = None
    category_id = request.args.get('category_id')
    allCategories = dao.get_all_categories()
    allProducts = dao.get_products_by_category(category_id=category_id, limit=16)
    productsSeller = dao.get_products_bestSeller(12)
    return render_template('index.html', user=user, countCart=countCart, products=allProducts, categories=allCategories,
                           productsSeller=productsSeller)


@app.route("/employee")
def employee_home():
    return render_template('employee-home.html')


@app.route("/login")
def show_login():
    return render_template("login.html")


@app.route("/auth/login", methods=['POST'])
def user_login():
    username = request.form.get('username')
    password = request.form.get("password")

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
        id_user = int(current_user.user_id)
        users = dao.get_inf_user(id_user)
        session['roles'] = str(current_user.users_role_id)
        category_id = request.args.get('category_id')
        allCategories = dao.get_all_categories()
        allProducts = dao.get_products_by_category(category_id=category_id, limit=28)
        productsSeller = dao.get_products_bestSeller(12)
        if current_user.users_role_id == UsersRole.ADMIN:
            return redirect("/admin")
        elif current_user.users_role_id == UsersRole.EMPLOYEE:
            return redirect("/employee")
        else:
            return render_template('index.html', user=users, products=allProducts, categories=allCategories,
                                   productsSeller=productsSeller)
    else:
        return render_template('login.html')


@app.route("/oauth-login", methods=['GET'])
def login_oauth():
    authorization_url, state = flow.authorization_url()
    print(authorization_url)
    return redirect(authorization_url)


@app.route("/callback", methods=['GET'])
def oauth_callback():
    try:
        user_oauth = dao.get_user_oauth()
        print(user_oauth)
        email = user_oauth['email']
        account = Accounts.query.filter_by(email=email).first()
        if account is None:
            import hashlib
            password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
            fullname = user_oauth['name']
            image = user_oauth['picture']
            users = Users(name=fullname, email=email, photoPath=image)
            db.session.add(users)
            db.session.flush()
            customer = Customers(id=users.id)
            db.session.add(customer)
            accountNew = Accounts(name=fullname, email=email, password=password, user_id=users.id)
            db.session.add(accountNew)
            db.session.commit()
        login_user(account)
        if account.users_role_id == UsersRole.ADMIN:
            return redirect('/admin')
        elif account.users_role_id == UsersRole.EMPLOYEE:
            return redirect('/employee')
        else:
            return redirect('/')
    except Exception as err:
        print(err)
        return redirect("/")
    return redirect("/")


# Cart------------------------------------------->
@app.route("/cart", methods=["GET"])
def view_cart():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        countCart = dao.get_count_cart(user_id)
        listProducts = dao.get_products_to_cart(user_id)
        return render_template('carts.html', user=user, countCart=countCart, listProducts=listProducts)
    else:
        return redirect(url_for('show_login'))
@app.route("/get-count-cart/<int:user_id>")
def get_count(user_id):
    count = dao.get_count_cart(user_id)
    return jsonify({"count": count})


@app.route("/cart/remove", methods=['DELETE'])
def remove_cart():
    cart_id = request.args.get('cart_id')
    success = dao.remove_product_to_cart(cart_id)
    if success:
        return jsonify({"message": "Sản phẩm đã được xóa khỏi giỏ hàng"}), 200
    else:
        return jsonify({"message": "Có lỗi xảy ra khi xóa sản phẩm"}), 500


@app.route("/cart/add-default", methods=['POST', 'GET'])
def add_cart_default():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        product_id = request.args.get('product_id')
        dao.add_to_cart(user_id, product_id, 1)
        return jsonify({"message": "Sản phẩm đã được thêm vào giỏ hàng"})
    else:
        return redirect(url_for('show_login'))


@app.route("/cart/add", methods=['POST', 'GET'])
def add_cart():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        product_id = request.args.get('product_id')
        quantity = request.args.get('quantity')
        dao.add_to_cart(user_id, product_id, quantity)
        return jsonify({'message': 'Sản phẩm đã được thêm vào giỏ hàng thành công!'})
    else:
        return jsonify({'error': 'not_authenticated'}), 401


@app.route("/cart/update", methods=['POST'])
def update_cart():
    data = request.get_json()
    print(data)
    cart_id = data.get('cart_id')
    quantity = data.get('quantity')
    if cart_id and quantity:
        dao.update_quantity_cart(cart_id=cart_id, new_quantity=quantity)
        return jsonify({"message": "Quantity updated successfully"}), 200
    return jsonify({"error": "Invalid input"}), 400

@app.route("/checkout-order", methods=['GET', 'POST'])
def payment_order():
    pass


@app.route("/logout")
def user_logout():
    logout_user()
    return redirect(url_for('show_login'))


@login.user_loader
def load_user(user_id):
    return Accounts.query.get(user_id)


@app.route("/auth/register", methods=['POST'])
def user_register():
    fullName = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    dao.add_account(fullName, username, password, email)
    return redirect(url_for('show_login'))


@app.route("/account/forgot", methods=['POST', 'GET'])
def user_forgot():
    forgorEmail = request.form.get('forgotEmail')
    return redirect(url_for('show_login'))


@app.route("/categories", methods=["GET"])
def view_categories():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        countCart = dao.get_count_cart(user_id)
    else:
        user = None
        countCart = None
    category_id = request.args.get('category_id')
    category = dao.get_category(category_id)
    allCategories = dao.get_all_categories()
    allProducts = dao.get_product_by_caterory_all(category_id)
    return render_template('categories.html', user=user, countCart=countCart, products=allProducts, category=category,
                           categories=allCategories, current_category_id=category_id)


# Product--------------------------------------->
@app.route("/products", methods=["GET"])
def view_product_detail():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        countCart = dao.get_count_cart(user_id)
    else:
        user = None
        countCart = None
    product_id = request.args.get('product_id')
    product = dao.get_product(product_id)
    category_id = product.category_id
    category = dao.get_category(category_id)
    productsNeight = dao.get_products_by_category(category_id, 8)
    return render_template('detail-product.html', user=user, countCart=countCart, product=product, category=category,
                           productsNeight=productsNeight)


@app.route("/products/<category_id>", methods=['GET'])
def view_products_by_category(category_id):
    if category_id:
        products = Products.query.filter(Products.category_id == category_id).limit(8).all()
    else:
        products = Products.query.limit(12).all()

    return render_template('products_list.html', products=products)


@app.route("/user/account/profile", methods=['GET', 'POST'])
def view_profile():
    pass


@app.route("/contact", methods=['GET', 'POST'])
def view_contact():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        countCart = dao.get_count_cart(user_id)
    else:
        user = None
        countCart = None
    return render_template('contact.html', countCart=countCart, user=user)


@app.route("/blog", methods=['GET'])
def view_blog():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        countCart = dao.get_count_cart(user_id)
    else:
        user = None
        countCart = None
    return render_template('blog.html', countCart=countCart, user=user)


# checkout--------------------------------------------
@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    user_id = int(current_user.user_id)
    user = dao.get_inf_user(user_id)
    subtotal = request.form.get("subtotal")
    tax = request.form.get("tax")
    total = request.form.get("total")
    l_cartId = request.form.getlist('cart_id')
    print(l_cartId)
    l_address= dao.get_address_by_user_id(int(current_user.user_id))
    return render_template('checkout.html',user=user, subtotal=subtotal, tax=tax, total=total, l_address=l_address, l_cartId=l_cartId)


@app.route('/confirm-checkout', methods=["POST"])
def confirm_checkout():
    try:

        data = request.get_json()
        customer_id = int(current_user.user_id)
        address_id = data.get('address_id')
        total = data.get('total')
        paymentMethod = data.get('paymentMethod')
        l_cart = data.get('l_cart')

        # Validate required fields
        if not address_id or not total or not paymentMethod or not l_cart:
            return jsonify({"error": "Missing required fields"}), 400

        # Call your DAO method to handle order creation
        dao.create_order_customer(customer_id=customer_id, address_id=address_id, total=total,
                                  paymentMethods=paymentMethod, l_cartId=l_cart)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500
@app.route("/success-order", methods=['GET'])
def success_order():
    user_id = int(current_user.user_id)
    user = dao.get_inf_user(user_id)
    return render_template("success-checkout.html", user=user)

@app.route("/employee", methods=['GET'])
def view_home_employee():
    return render_template("employee-home.html")


@app.route("/employee/profile", methods=['GET'])
def view_employee_profile():
    return render_template("employee-profile.html")


@app.route("/employee/help-customer", methods=['GET'])
def view_customercare():
    return render_template("customer-care.html")


@app.route("/employee/order-manager", methods=['GET'])
def view_order_manager():
    listOrders = dao.get_all_orders()
    order_confirm = dao.get_all_orders_confirm()
    return render_template("employee-ordermanage.html", orders=listOrders, orderConfirms=order_confirm)


@app.route("/employee/confirm-order")
def confirm_order():
    order_id = request.args.get('order_id')
    dao.chang_active_order(order_id)
    return redirect(url_for('view_order_manager'))


@app.route("/employee/confirm-order-list", methods=['GET'])
def confirm_order_list():
    list_id = request.args.get('list_id', '')
    # Chuyển chuỗi thành danh sách
    if list_id:
        order_ids = list_id.split(',')
    else:
        return redirect(url_for('view_order_manager'))
    if not order_ids:
        return redirect(url_for('view_order_manager'))
    dao.chang_active_order_list(order_ids)
    print(f"Processing orders: {order_ids}")
    return redirect(url_for('view_order_manager'))


@app.route("/employye/order-tracking", methods=['GET', 'POST'])
def view_order_tracking():
    order_id = request.args.get('order_id')
    order = dao.get_orders_by_id(order_id)
    return render_template("employee-ordertracking.html", order=order)


@app.route("/employee/payment", methods=['GET'])
def view_payment():
    products = dao.get_all_products()
    return render_template("payment.html", products=products)


@app.route("/employee/confirm-payment", methods=['POST', 'GET'])
def confirm_payment():
    hoten = request.form.get('hoten')
    ngaySinh = request.form.get('ngaySinh')
    phone = request.form.get('phone')
    diaChi = request.form.get('diaChi')
    product_ids = request.form.getlist('product_id')
    quantities = request.form.getlist('quantity')
    if current_user.is_authenticated:
        employee_id = current_user.user_id
    else:
        employee_id = 2


    dao.create_order(name=hoten, ngaySinh=ngaySinh, diaChi=diaChi, phone=phone, l_soLuong=quantities,
                     l_productId=product_ids, employee_id=employee_id)
    return redirect(url_for('view_order_manager'))


if __name__ == "__main__":
    from AppShop import admin

    app.run(host='localhost', port=5001, debug=True)
