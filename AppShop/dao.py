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
#Carts-------------------------------------------->
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

def add_to_cart(user_id, product_id, quantity):
    cart= Carts(customer_id=user_id, product_id=product_id, quantity=quantity)
    db.session.add(cart)
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


#Users------------------------------------------->
def get_inf_user(id):
    return Users.query.filter(Users.id.__eq__(id)).first()



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

def get_all_orders():
    orders = db.session.query(
        Orders.id,
        Users.name.label('user_name'),
        Shippers.companyName.label('shipper_name'),
        BillingAddress.address.label('billing_address'),
        Orders.paymentMethods,
        Orders.orderDate,
        Orders.active,
        Orders.totalAmount
    ).join(Users, Orders.customer_id == Users.id) \
     .join(Shippers, Orders.shipper_id == Shippers.id) \
     .join(BillingAddress, Orders.billingAddress_id == BillingAddress.id) \
     .filter(Orders.active == False) \
     .all()

    return orders

def get_orders_by_id(order_id):
    # Tạo alias cho bảng Users
    orders = db.session.query(
        Orders.id,
        Users.name.label('customer_name'),  # Giả định rằng đây là tên khách hàng
        Shippers.companyName.label('shipper_name'),
        BillingAddress.address.label('billing_address'),
        BillingAddress.phone.label('phone'),
        Orders.paymentMethods,
        Orders.orderDate,
        Orders.active,
        Orders.totalAmount
    ).join(Users, Orders.customer_id == Users.id) \
     .join(Shippers, Orders.shipper_id == Shippers.id) \
     .join(BillingAddress, Orders.billingAddress_id == BillingAddress.id) \
     .filter(Orders.id == order_id) \
     .first()  # Dùng .first() để lấy một kết quả duy nhất

    return orders








