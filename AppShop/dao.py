from sqlalchemy.orm import aliased

from AppShop import db
from AppShop.models import Categories, Products,Accounts,Users,Carts,Customers,Orders,Shippers,BillingAddress
import hashlib

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Accounts.query.filter(Accounts.username.__eq__(username.strip()), Accounts.password.__eq__(password)).first()
#Categories------------------------------------->
def get_all_categories():
    return Categories.query.all()
def get_category(id):
    return Categories.query.filter(Categories.id.__eq__(id)).first()
#Products---------------------------------------->
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
        products= Products.query.filter(Products.category_id.__eq__(category_id))
    else:
        products= Products.query.all()
    return products[:limit]

def get_product(id):
    return Products.query.filter(Products.id.__eq__(id)).first()