from AppShop import app, dao, login, flow, socketio
from AppShop.models import UsersRole, Accounts, Users, Products, Customers, Messages, FeedbackProduct
from flask import render_template, session, flash, jsonify, redirect, request, url_for
from flask_login import login_user, current_user, logout_user
from AppShop.admin import *
from flask_socketio import SocketIO, emit


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
            account = Accounts(name=fullname, email=email, password=password, user_id=users.id)
            db.session.add(account)
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

@app.route('/search')
def search():
    q = request.args.get('q')
    if q:
        products = Products.query.filter(Products.name.ilike(f'%{q}%')).all()
    else:
        products = Products.query.all()

    categories = Categories.query.all()

    return render_template('categories.html', products=products, categories=categories)


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
    lFeedback = dao.get_product_feedback(product_id)
    category_id = product.category_id
    category = dao.get_category(category_id)
    productsNeight = dao.get_products_by_category(category_id, 8)
    return render_template('detail-product.html', lFeedback=lFeedback, user=user, countCart=countCart, product=product,
                           category=category,
                           productsNeight=productsNeight)


@app.route("/products/<category_id>", methods=['GET'])
def view_products_by_category(category_id):
    if category_id:
        products = Products.query.filter(Products.category_id == category_id).limit(8).all()
    else:
        products = Products.query.limit(12).all()

    return render_template('products_list.html', products=products)


@app.route('/submit_review', methods=['POST'])
def submit_review():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        rating = request.form.get('rating')
        comment = request.form.get('message')
        if current_user.is_authenticated:
            new_feedback = FeedbackProduct(
                product_id=product_id,
                user_id=current_user.id,
                rating=rating,
                comment=comment
            )
            db.session.add(new_feedback)
            db.session.commit()
            flash('Đánh giá của bạn đã được gửi!', 'success')
            return redirect(url_for('view_product_detail', product_id=product_id))
        else:
            flash('Bạn cần đăng nhập để gửi đánh giá.', 'error')
    return redirect(url_for('view_product_detail', product_id=product_id))

@app.route("/user/account/profile", methods=['GET', 'POST'])
def view_profile():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('show_login'))


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


@app.route("/history-order", methods=['GET'])
def view_history_order():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        history_order = dao.get_orders_with_products(user_id)
        countCart = dao.get_count_cart(user_id)
        return render_template('order-history.html', orders=history_order, user=user, countCart=countCart)


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
    l_address = dao.get_address_by_user_id(int(current_user.user_id))
    return render_template('checkout.html', user=user, subtotal=subtotal, tax=tax, total=total, l_address=l_address,
                           l_cartId=l_cartId)


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
    user_id = int(current_user.user_id)
    user = dao.get_inf_user(user_id)
    return render_template("employee-home.html", user=user)


@app.route("/employee/profile", methods=['GET'])
def view_employee_profile():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)

        return render_template('employee-profile.html', user=user)
    else:
        return redirect(url_for('show_login'))


@app.route("/employee/help-customer", methods=['GET', 'POST'])
def view_customercare():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        accountId = dao.get_account_customer()
        return render_template('customer-care.html', user=user, accounts=accountId)
    else:
        return redirect(url_for('show_login'))


@app.route("/employee/order-manager", methods=['GET'])
def view_order_manager():
    user_id = int(current_user.user_id)
    user = dao.get_inf_user(user_id)
    listOrders = dao.get_all_orders()
    order_confirm = dao.get_all_orders_confirm()
    return render_template("employee-ordermanage.html", orders=listOrders, orderConfirms=order_confirm, user=user)


@app.route("/employee/confirm-order")
def confirm_order():
    order_id = request.args.get('order_id')
    dao.chang_active_order(order_id)
    return redirect(url_for('view_order_manager'))


@app.route("/remove-order", methods=['POST', 'GET'])
def remove_order():
    order_id = request.args.get('order_id')
    result = dao.delete_order(order_id)
    if result:
        return redirect(url_for('view_order_manager'))
    else:
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
    user_id = int(current_user.user_id)
    user = dao.get_inf_user(user_id)
    products = dao.get_all_products()
    return render_template("payment.html", products=products, user=user)


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


# Invoice-----------------------------------------------------
@app.route("/employee/invoice")
def view_invoice():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        currentDate = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        order_id = request.args.get('order_id')
        order = dao.get_order_confirm(order_id)
        orderDetail = dao.get_order_detail(order_id)
        return render_template('invoice.html', order=order, order_detail=orderDetail, currentDate=currentDate,
                               user=user)
    else:
        return redirect(url_for('show_login'))


# chatbox----------------------------------------------
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    if current_user.users_role_id == UsersRole.CUSTOMER:
        message = Messages(
            buyer_id=data['buyer_id'],
            content=data['content']
        )
    else:
        message = Messages(
            buyer_id=data['buyer_id'],
            content=data['content'],
            serder=True
        )
    db.session.add(message)
    db.session.commit()
    formatted_timestamp = message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    socketio.emit('new_message', {
        'timestamp': formatted_timestamp,
        'content': message.content,
        'buyer_id': message.buyer_id,
        'serder': message.serder
    })
    return jsonify({'status': 'success'}), 200


@app.route('/get_messages/<int:buyer_id>', methods=['GET'])
def get_messages(buyer_id):
    messages = Messages.query.filter_by(buyer_id=buyer_id).all()
    return jsonify([{
        'serder': msg.serder,
        'content': msg.content,
        'buyer_id': msg.buyer_id,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Định dạng thời gian
    } for msg in messages]), 200


@app.route("/chat-box", methods=['GET', 'POST'])
def chat_box():
    if current_user.is_authenticated:
        account_id = int(current_user.id)
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
    return render_template('chatbox.html', account_id=account_id, user=user)


@app.route("/add/address", methods=['POST', 'GET'])
def create_address():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        city = request.form.get('city')
        address = request.form.get('address')
        address_detail = request.form.get('addressDetail')
        phone = request.form.get('phone')
        if not firstname or not lastname or not address or not city or not phone:
            return jsonify({'success': False, 'error': 'Please fill in all required fields.'}), 400
        new_address = dao.create_address_customer(customer_id=user_id, name=f"{firstname} {lastname}", phone=phone,
                                                  address=address, address_detail=address_detail)

        if new_address:
            return jsonify({
                'success': True,
                'new_address': {
                    'id': new_address.id,
                    'name': new_address.name,
                    'phone': new_address.phone,
                    'addressDetail': new_address.addressDetail
                }
            }), 201
        else:
            return jsonify({'success': False, 'error': 'Failed to create address.'}), 500
    else:
        return jsonify({'success': False, 'error': 'You need to log in first!'}), 401


if __name__ == "__main__":
    from AppShop import admin

    socketio.run(app, host='localhost', port=5001, debug=True, allow_unsafe_werkzeug=True)
