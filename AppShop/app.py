from AppShop import app,dao
from AppShop.models import Products
from AppShop.models import UsersRole,Accounts
from flask import render_template, session, flash, jsonify, redirect, request, url_for
# from flask_login import login_user, current_user, logout_user
from AppShop.admin import *

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    from AppShop import admin

    app.run(debug=True)