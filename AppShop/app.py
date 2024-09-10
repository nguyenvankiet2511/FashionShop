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
    return render_template('index.html', user=user,countCart=countCart, products=allProducts, categories=allCategories,
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
@app.route("/carts")
def view_cart():
    return render_template('carts.html')
if __name__ == "__main__":
    from AppShop import admin

    app.run(debug=True)