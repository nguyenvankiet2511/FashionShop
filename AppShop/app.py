from AppShop import app,dao,login
from AppShop.models import Products
from AppShop.models import UsersRole,Accounts
from flask import render_template, session, flash, jsonify, redirect, request, url_for
from flask_login import login_user, current_user, logout_user
from AppShop.admin import *

@app.route("/")
def home():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        countCart= dao.get_count_cart(user_id)
    else:
        user = None
        countCart=None
    category_id = request.args.get('category_id')
    allCategories = dao.get_all_categories()
    allProducts = dao.get_products_by_category(category_id=category_id, limit=16)
    productsSeller = dao.get_products_bestSeller(12)
    return render_template('invoice.html', user=user,countCart=countCart, products=allProducts, categories=allCategories,
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
        productsSeller= dao.get_products_bestSeller(12)
        if current_user.users_role_id == UsersRole.ADMIN:
            return redirect("/admin")
        elif current_user.users_role_id == UsersRole.EMPLOYEE:
            return redirect("/employee")
        else:
            return render_template('index.html',user=users, products=allProducts, categories=allCategories, productsSeller=productsSeller)
    else:
        return render_template('login.html')



#Cart------------------------------------------->
@app.route("/cart", methods=["GET"])
def view_cart():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        countCart = dao.get_count_cart(user_id)
        listProducts= dao.get_products_to_cart(user_id)
        return render_template('carts.html',user=user,countCart=countCart, listProducts=listProducts)
    else:
        return redirect(url_for('show_login'))


@app.route("/cart/remove", methods=['DELETE'])
def remove_cart():
    cart_id = request.args.get('cart_id')
    success = dao.remove_product_to_cart(cart_id)
    if success:
        return jsonify({"message": "Sản phẩm đã được xóa khỏi giỏ hàng"}), 200
    else:
        return jsonify({"message": "Có lỗi xảy ra khi xóa sản phẩm"}), 500

@app.route("/cart/add-default", methods=['POST','GET'])
def add_cart_default():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        product_id = request.args.get('product_id')
        dao.add_to_cart(user_id, product_id, 1)
        return jsonify({"message": "Sản phẩm đã được thêm vào giỏ hàng"})
    else:
        return redirect(url_for('show_login'))
@app.route("/cart/add", methods=['POST','GET'])
def add_cart():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        product_id = request.args.get('product_id')
        quantity = request.args.get('quantity')
        dao.add_to_cart(user_id, product_id, quantity)
        return jsonify({'message': 'Sản phẩm đã được thêm vào giỏ hàng thành công!'})
    else:
        return jsonify({'error': 'not_authenticated'}), 401

@app.route("/checkout-order", methods=['GET','POST'])
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
    fullName= request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    dao.add_account(fullName, username, password, email)
    return redirect(url_for('show_login'))

@app.route("/account/forgot", methods=['POST','GET'])
def user_forgot():
    forgorEmail= request.form.get('forgotEmail')
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
    category= dao.get_category(category_id)
    allCategories = dao.get_all_categories()
    allProducts = dao.get_product_by_caterory_all(category_id)
    return render_template('categories.html', user=user, countCart=countCart,products=allProducts,category=category, categories=allCategories,current_category_id=category_id)

#Product--------------------------------------->
@app.route("/products", methods=["GET"])
def view_product_detail():
    if current_user.is_authenticated:
        user_id = int(current_user.user_id)
        user = dao.get_inf_user(user_id)
        countCart = dao.get_count_cart(user_id)
    else:
        user=None
        countCart = None
    product_id = request.args.get('product_id')
    product= dao.get_product(product_id)
    category_id= product.category_id
    category = dao.get_category(category_id)
    productsNeight= dao.get_products_by_category(category_id,8)
    return render_template('detail-product.html',user=user,countCart=countCart,product=product,category=category, productsNeight=productsNeight)

@app.route("/products/<category_id>", methods=['GET'])
def view_products_by_category(category_id):
    if category_id:
        products = Products.query.filter(Products.category_id == category_id).limit(8).all()
    else:
        products = Products.query.limit(12).all()

    return render_template('products_list.html', products=products)

@app.route("/user/account/profile", methods=['GET','POST'])
def view_profile():
    pass
@app.route("/contact", methods=['GET','POST'])
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
@app.route("/employee", methods=['GET'])
def view_home_employee():
    return render_template("employee-home.html")

@app.route("/employee/profile", methods=['GET'])
def view_employee_profile():
   return render_template("employee-profile.html")
@app.route("/employee/help-customer",methods=['GET'])
def view_customercare():
    return render_template("customer-care.html")
@app.route("/employee/order-manager", methods=['GET'])
def view_order_manager():
    listOrders= dao.get_all_orders()
    order_confirm= dao.get_all_orders_confirm()
    return render_template("employee-ordermanage.html",orders=listOrders,orderConfirms= order_confirm)
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

@app.route("/employye/order-tracking", methods=['GET','POST'])
def view_order_tracking():
    order_id = request.args.get('order_id')
    order = dao.get_orders_by_id(order_id)
    return render_template("employee-ordertracking.html", order=order)
@app.route("/employee/payment", methods=['GET'])
def view_payment():
    products = dao.get_all_products()
    return render_template("payment.html",products=products)
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

    app.run(debug=True)