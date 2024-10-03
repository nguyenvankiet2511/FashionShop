import hashlib
from AppShop import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text, Enum, Double
from sqlalchemy.orm import relationship, backref
from datetime import datetime, timedelta


class UsersRole(UserEnum):
    ADMIN = 1
    EMPLOYEE = 2
    CUSTOMER = 3


class Accounts(db.Model, UserMixin):
    __tablename__ = 'Accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))
    active = Column(Boolean)
    users_role_id = Column(Enum(UsersRole), default=UsersRole.CUSTOMER)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)

    # Đổi tên backref để tránh xung đột
    feedback_customers = relationship("FeedbackCustomers", backref="account")
    messages = relationship("Messages", backref="account")
    feedback_products = relationship("FeedbackProduct", backref="account")


class Users(db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    gender = Column(Boolean)
    birthDate = Column(DateTime)
    phone = Column(String(12))
    email = Column(String(255))
    address = Column(String(255))
    photoInf = Column(Text)
    photoPath = Column(String(255))
    account = relationship('Accounts', backref='user', lazy=True)
    employees = relationship("Employees", uselist=False, back_populates="user")
    customers = relationship("Customers", uselist=False, back_populates="user")


class Employees(db.Model):
    __tablename__ = 'Employees'

    id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    degree = Column(String(150), default="Không")
    # ///
    user = relationship("Users", back_populates="employees")
    orders = relationship("Orders", backref="employee")
    order_returns = relationship("OrderReturn", backref="employee")


class Customers(db.Model):
    __tablename__ = 'Customers'

    id = Column(Integer, ForeignKey('Users.id'), primary_key=True)

    user = relationship("Users", back_populates="customers")
    billing_addresses = relationship("BillingAddress", backref="customer")
    orders = relationship("Orders", backref="customer")
    carts = relationship("Carts", backref="customer")


class BillingAddress(db.Model):
    __tablename__ = 'BillingAddress'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(12), nullable=False)
    address = Column(Text)
    addressDetail = Column(Text)
    customer_id = Column(Integer, ForeignKey('Customers.id'), nullable=False)

    order = relationship("Orders", backref="billing_address")


class Categories(db.Model):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    products = relationship("Products", backref="category")
    photoCategory= Column(String(255))


class Products(db.Model):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    price = Column(Double, default=0)
    description = Column(Text)
    imageProduct = Column(String(255))
    category_id = Column(Integer, ForeignKey('Categories.id'), nullable=False)
    unitsInStock = Column(Integer, default=0)
    discount = Column(Integer, default=0)
    createdDate = Column(DateTime)
    updatedDate = Column(DateTime)

    feedback_products = relationship("FeedbackProduct", backref="product")
    order_details = relationship("OrderDetails", backref="product")
    carts = relationship("Carts", backref="product")


class FeedbackCustomers(db.Model):
    __tablename__ = 'FeedbackCustomers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('Accounts.id'), nullable=False)
    comment = Column(Text)


class FeedbackProduct(db.Model):
    __tablename__ = 'FeedbackProduct'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Accounts.id'))
    product_id = Column(Integer, ForeignKey('Products.id'))
    rating = Column(Integer)
    comment = Column(Text)
    createDate= Column(DateTime, default=datetime.now())


class Shippers(db.Model):
    __tablename__ = 'Shippers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    companyName = Column(String(255), nullable=False)
    phone = Column(String(12))

    orders = relationship("Orders", backref="shipper")


class Orders(db.Model):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('Customers.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('Employees.id'))
    shipper_id = Column(Integer, ForeignKey('Shippers.id'))
    billingAddress_id = Column(Integer, ForeignKey('BillingAddress.id'))
    paymentMethods = Column(String(150), default="Mua hàng trực tiếp")
    orderDate = Column(DateTime, default=datetime.now())
    orderComfirm = Column(DateTime)
    active = Column(Boolean)
    totalAmount = Column(Double, default=0)

    order_details = relationship("OrderDetails", backref="order")
    order_returns = relationship("OrderReturn", backref="order")


class OrderDetails(db.Model):
    __tablename__ = 'OrderDetails'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('Orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('Products.id'), nullable=False)
    quantity = Column(Integer)
    price = Column(Double, default=0)
    discount = Column(Integer, default=0)


class Carts(db.Model):
    __tablename__ = 'Carts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('Customers.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('Products.id'), nullable=False)
    quantity = Column(Integer)
    price = Column(Numeric)
    discount = Column(Integer)


class Messages(db.Model):
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, ForeignKey('Accounts.id'), nullable=False)
    serder= Column(Boolean, default=0)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Message {self.id} from Buyer {self.buyer_id}>'



class OrderReturn(db.Model):
    __tablename__ = 'OrderReturn'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('Orders.id'), nullable=False)
    reason = Column(Text)
    returnDate = Column(DateTime)
    active = Column(Boolean)
    status = Column(String(50), default="Đang chờ xử lý")
    employee_id = Column(Integer, ForeignKey('Employees.id'))
    processedDate = Column(DateTime)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        users_data = [
            Users(name="Nguyễn Văn An", gender=True, birthDate=datetime(1980, 5, 15), phone="123-456-7890",
                  email="an.nguyen@example.com", address="123 Đường Trần Phú, Phường 7, Quận 5, TP. Hồ Chí Minh",
                  photoPath="avatar-02.jpg"),

            Users(name="Lê Thu Cúc", gender=False, birthDate=datetime(1990, 8, 22), phone="234-567-8901",
                  email="cuc.le@example.com", address="456 Đường Lê Lợi, Phường 10, Quận 3, TP. Hà Nội",
                  photoPath="avatar-01.jpg"),
            Users(name="Đinh Quốc Anh", gender=True, birthDate=datetime(1983, 9, 9), phone="890-123-4567",
                  email="anh.dinh@example.com", address="505 Đường Võ Thị Sáu, Phường 4, TP. Biên Hòa",
                  ),

            Users(name="Trần Văn Bảo", gender=True, birthDate=datetime(1975, 3, 5), phone="456-789-0123",
                  email="bao.tran@example.com", address="101 Đường Hoàng Hoa Thám, Phường 2, TP. Đà Nẵng",
                  photoPath="avatar-05.jpg"),

            Users(name="Phạm Thu Hà", gender=False, birthDate=datetime(1988, 7, 19), phone="567-890-1234",
                  email="ha.pham@example.com", address="202 Đường Hai Bà Trưng, Phường 6, TP. Cần Thơ",
                  photoPath="avatar-03.jpg"),
            Users(name="Nguyễn Thị Mai", gender=False, birthDate=datetime(1985, 12, 30), phone="345-678-9012",
                  email="mai.nguyen@example.com", address="789 Đường Nguyễn Trãi, Phường 5, Quận 1, TP. Hồ Chí Minh",
                  photoPath="avatar-04.jpg"),

            Users(name="Vũ Hoàng Nam", gender=True, birthDate=datetime(1995, 11, 25), phone="678-901-2345",
                  email="nam.vu@example.com", address="303 Đường Lê Văn Sỹ, Phường 14, Quận Phú Nhuận, TP. Hồ Chí Minh",
                  photoPath="avatar-01.jpg"),

            Users(name="Nguyễn Thị Hoa", gender=False, birthDate=datetime(1992, 2, 14), phone="789-012-3456",
                  email="hoa.nguyen@example.com",
                  address="404 Đường Điện Biên Phủ, Phường 15, Quận Bình Thạnh, TP. Hồ Chí Minh",
                  photoPath="avatar-05.jpg"),

            Users(name="Phạm Khánh Linh", gender=False, birthDate=datetime(2000, 4, 21), phone="901-234-5678",
                  email="linh.pham@example.com", address="606 Đường Phạm Ngũ Lão, Phường 3, TP. Vũng Tàu",
                  ),

            Users(name="Ngô Đức Huy", gender=True, birthDate=datetime(1987, 10, 30), phone="012-345-6789",
                  email="huy.ngo@example.com",
                  address="707 Đường Lý Thường Kiệt, Phường 12, Quận Tân Bình, TP. Hồ Chí Minh",
                  )

        ]
        db.session.add_all(users_data)
        db.session.commit()
        # Emplyoee
        employees_data = [
            Employees(id=1),
            Employees(id=2),
            Employees(id=3),
            Employees(id=4),
            Employees(id=5)
        ]
        db.session.add_all(employees_data)
        db.session.commit()
        #
        customers_data = [
            Customers(id=6),
            Customers(id=7),
            Customers(id=8),
            Customers(id=9),
            Customers(id=10)
        ]
        db.session.add_all(customers_data)
        db.session.commit()
        # Categories
        categories_data = [
            Categories(name='Áo sơ mi', photoCategory='category-shirt.png'),
            Categories(name='Quần jeans', photoCategory='category-jeans.jpg'),
            Categories(name='Áo khoác', photoCategory='category-gallery.jpg'),
            Categories(name='Giày thể thao', photoCategory='category-shoes.jpg'),
            Categories(name='Đồng hồ', photoCategory='category-watched.jpg'),
            Categories(name='Phụ kiện thời trang', photoCategory='category-other.jpg')
        ]
        db.session.add_all(categories_data)
        db.session.commit()



        address_data = [
            BillingAddress(name='Nguyen Van A', phone='0912345678', address='123 ABC Street',
                           addressDetail='Apartment 5A', customer_id=6),
            BillingAddress(name='Tran Thi B', phone='0987654321', address='456 DEF Avenue',
                           addressDetail='House 12', customer_id=6),
            BillingAddress(name='Le Van C', phone='0923456789', address='789 GHI Road',
                           addressDetail='Suite 3', customer_id=6),
            BillingAddress(name='Pham Thi D', phone='0911123456', address='135 JKL Street',
                           addressDetail='Villa 9', customer_id=6),
            BillingAddress(name='Vu Thi E', phone='0933456789', address='246 MNO Boulevard',
                           addressDetail='Flat 21B', customer_id=6)
        ]
        db.session.add_all(address_data)
        db.session.commit()

        # Products
        products_data = [
            Products(name='Áo sơ mi trắng', price=299000, description='Áo sơ mi trắng chất liệu cotton cao cấp',
                     imageProduct='shirt-5.jpg', category_id=1, unitsInStock=50, discount=10,
                     createdDate=datetime(2024, 1, 1), updatedDate=datetime(2024, 8, 1)),
            Products(name='Áo sơ mi xanh', price=319000, description='Áo sơ mi xanh dương nhẹ nhàng',
                     imageProduct='shirt-3.jpg', category_id=1, unitsInStock=30, discount=5,
                     createdDate=datetime(2024, 1, 10), updatedDate=datetime(2024, 8, 2)),
            Products(name='Áo sơ mi kẻ sọc', price=329000, description='Áo sơ mi kẻ sọc hiện đại',
                     imageProduct='shirt-6.jpg', category_id=1, unitsInStock=20, discount=15,
                     createdDate=datetime(2024, 2, 1), updatedDate=datetime(2024, 8, 3)),
            Products(name='Áo sơ mi họa tiết', price=339000, description='Áo sơ mi họa tiết đa dạng',
                     imageProduct='shirt-7.jpg', category_id=1, unitsInStock=45, discount=15,
                     createdDate=datetime(2024, 7, 1), updatedDate=datetime(2024, 8, 12)),

            Products(name='Quần jeans xanh', price=399000, description='Quần jeans chất liệu denim bền bỉ',
                     imageProduct='trousers-2.jpg', category_id=2, unitsInStock=40, discount=20,
                     createdDate=datetime(2024, 3, 1), updatedDate=datetime(2024, 8, 4)),
            Products(name='Quần jeans đen', price=419000, description='Quần jeans đen thời trang',
                     imageProduct='trousers-1.jpg', category_id=2, unitsInStock=35, discount=25,
                     createdDate=datetime(2024, 3, 10), updatedDate=datetime(2024, 8, 5)),
            Products(name='Quần shorts', price=349000, description='Quần shorts mùa hè thoải mái',
                     imageProduct='trousers-3.jpg', category_id=2, unitsInStock=50, discount=10,
                     createdDate=datetime(2024, 7, 10), updatedDate=datetime(2024, 8, 13)),

            Products(name='Áo khoác da', price=799000, description='Áo khoác da cao cấp cho mùa đông',
                     imageProduct='shirt-8.jpg', category_id=3, unitsInStock=25, discount=30,
                     createdDate=datetime(2024, 4, 1), updatedDate=datetime(2024, 8, 6)),
            Products(name='Áo khoác bomber', price=729000, description='Áo khoác bomber kiểu dáng trẻ trung',
                     imageProduct='shirt-4.jpg', category_id=3, unitsInStock=30, discount=10,
                     createdDate=datetime(2024, 4, 15), updatedDate=datetime(2024, 8, 7)),
            Products(name='Áo khoác denim', price=749000, description='Áo khoác denim trẻ trung',
                     imageProduct='shirt-2.png', category_id=3, unitsInStock=20, discount=5,
                     createdDate=datetime(2024, 8, 1), updatedDate=datetime(2024, 8, 14)),
            Products(name='Áo khoác hoodie', price=669000, description='Áo khoác hoodie ấm áp',
                     imageProduct='shirt-9.jpg', category_id=3, unitsInStock=45, discount=15,
                     createdDate=datetime(2024, 9, 1), updatedDate=datetime(2024, 8, 17)),

            Products(name='Giày thể thao hồng', price=899000, description='Giày thể thao hồng năng động',
                     imageProduct='shoes-8.png', category_id=4, unitsInStock=50, discount=5,
                     createdDate=datetime(2024, 5, 1), updatedDate=datetime(2024, 8, 8)),
            Products(name='Giày thể thao đen', price=919000, description='Giày thể thao đen cá tính',
                     imageProduct='shoes-6.jpg', category_id=4, unitsInStock=40, discount=10,
                     createdDate=datetime(2024, 5, 10), updatedDate=datetime(2024, 8, 9)),
            Products(name='Giày lười', price=699000, description='Giày lười thanh lịch', imageProduct='shoes-1.png',
                     category_id=4, unitsInStock=35, discount=20, createdDate=datetime(2024, 8, 10),
                     updatedDate=datetime(2024, 8, 15)),

            Products(name='Thắt lưng da', price=199000, description='Thắt lưng da sang trọng',
                     imageProduct='leather-1.jpg', category_id=6, unitsInStock=60, discount=15,
                     createdDate=datetime(2024, 6, 1), updatedDate=datetime(2024, 8, 10)),
            Products(name='Kính mát thời trang', price=299000, description='Kính mát phong cách',
                     imageProduct='sunglasses-1.jpg', category_id=6, unitsInStock=70, discount=20,
                     createdDate=datetime(2024, 6, 15), updatedDate=datetime(2024, 8, 11)),
            Products(name='Mũ lưỡi trai', price=149000, description='Mũ lưỡi trai phong cách', imageProduct='cap-1.jpg',
                     category_id=6, unitsInStock=80, discount=10, createdDate=datetime(2024, 8, 15),
                     updatedDate=datetime(2024, 8, 16)),
            Products(name='Kính mát Leyean', price=299000, description='Kính mát phong cách thương hiệu Leyean',
                     imageProduct='sunglasses-2.jpg', category_id=6, unitsInStock=70, discount=20,
                     createdDate=datetime(2024, 6, 15), updatedDate=datetime(2024, 8, 11)),
            Products(name='Túi đeo thời trang Oupica', price=299000, description='Túi đem phong cách',
                     imageProduct='bag-1.png', category_id=6, unitsInStock=70, discount=20,
                     createdDate=datetime(2024, 6, 15), updatedDate=datetime(2024, 8, 11)),
            Products(name='Đồng hồ nam Pasika', price=299000, description='Đồng hồ nam màu đen thương hiệu Pasiko',
                     imageProduct='watch-1.jpg', category_id=5, unitsInStock=70, discount=20,
                     createdDate=datetime(2024, 6, 15), updatedDate=datetime(2024, 8, 11)),
            Products(name='Áo sơ mi caro', price=309000, description='Áo sơ mi caro lịch lãm',
                     imageProduct='shirt-10.jpg', category_id=1, unitsInStock=25, discount=10,
                     createdDate=datetime(2024, 1, 20), updatedDate=datetime(2024, 8, 18)),
        ]

        db.session.add_all(products_data)
        db.session.commit()

        account_data = [
            Accounts(name="Nguyễn Văn An", email="an.nguyen@example.com",
                     username="admin", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_id=1,
                     users_role_id=UsersRole.ADMIN, active=True),

            Accounts(name="Lê Thu Cúc", email="cuc.le@example.com",
                     username="nhanvien1", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_id=2,
                     users_role_id=UsersRole.EMPLOYEE, active=True),

            Accounts(name="Trần Văn Bảo", email="bao.tran@example.com",
                     username="nhanvien2", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_id=4,
                     users_role_id=UsersRole.EMPLOYEE, active=True),

            Accounts(name="Nguyễn Thị Mai", email="mai.nguyen@example.com",
                     username="kh1", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_id=6,
                     users_role_id=UsersRole.CUSTOMER, active=True),

            Accounts(name="Hoàng Văn Nam", email="nam.hoang@example.com",
                     username="kh2", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_id=7,
                     users_role_id=UsersRole.CUSTOMER, active=True)

        ]

        db.session.add_all(account_data)
        db.session.commit()

        orders_data = [
            Orders(customer_id=6, employee_id=2,  billingAddress_id=1, paymentMethods="COD",
                   orderDate=datetime.now() - timedelta(days=2), active=False, totalAmount=1477150),
            Orders(customer_id=7, employee_id=3,  billingAddress_id=2, paymentMethods="Credit Card",
                   orderDate=datetime.now(), active=False, totalAmount=1467850),
            Orders(customer_id=6, employee_id=4,  billingAddress_id=3, paymentMethods="Bank Transfer",
                   orderDate=datetime.now() - timedelta(days=1), active=False, totalAmount=938350),
            Orders(customer_id=7, employee_id=5,  billingAddress_id=4, paymentMethods="Mua hàng trực tiếp",
                   orderDate=datetime(2024, 4, 25), orderComfirm=datetime(2024, 4, 26), active=True,
                   totalAmount=3747600),
            Orders(customer_id=6, employee_id=2,  billingAddress_id=5, paymentMethods="Paypal",
                   orderDate=datetime(2024, 2, 25), orderComfirm=datetime(2024, 2, 28), active=True,
                   totalAmount=1050150),
            Orders(customer_id=7, employee_id=2,  billingAddress_id=5, paymentMethods="COD",
                   orderDate=datetime(2023, 11, 25), orderComfirm=datetime(2023, 11, 29), active=True,
                   totalAmount=1350200),
            Orders(customer_id=6, employee_id=2,  billingAddress_id=5, paymentMethods="Paypal",
                   orderDate=datetime(2024, 10, 8), orderComfirm=datetime(2024, 10, 12), active=True,
                   totalAmount=826500),
            Orders(customer_id=6, employee_id=2,  billingAddress_id=5, paymentMethods="COD",
                   orderDate=datetime(2024, 12, 12), orderComfirm=datetime(2024, 12, 16), active=True,
                   totalAmount=717550),
            Orders(customer_id=7, employee_id=2,  billingAddress_id=5, paymentMethods="Paypal",
                   orderDate=datetime.now(), active=False, totalAmount=1240200),
            Orders(customer_id=6, employee_id=2, billingAddress_id=5, paymentMethods="COD",
                   orderDate=datetime.now(), active=False, totalAmount=945700),
            Orders(customer_id=7, employee_id=2,  billingAddress_id=5, paymentMethods="Mua hàng trực tiếp",
                   orderDate=datetime.now(), active=False, totalAmount=1506550),
            Orders(customer_id=7, employee_id=2,  billingAddress_id=5, paymentMethods="Mua hàng trực tiếp",
                   orderDate=datetime(2024, 3, 14), orderComfirm=datetime(2024, 3, 18), active=True,
                   totalAmount=3024800),

        ]
        db.session.add_all(orders_data)
        db.session.commit()

        order_details_data = [
            OrderDetails(order_id=1, product_id=1, quantity=2, price=299000, discount=10),  # Áo sơ mi trắng
            OrderDetails(order_id=1, product_id=3, quantity=3, price=329000, discount=15),  # Áo sơ mi kẻ sọc
            OrderDetails(order_id=2, product_id=6, quantity=1, price=419000, discount=25),  # Quần jeans đen
            OrderDetails(order_id=2, product_id=8, quantity=2, price=799000, discount=30),  # Áo khoác da
            OrderDetails(order_id=3, product_id=2, quantity=1, price=319000, discount=5),  # Áo sơ mi xanh
            OrderDetails(order_id=3, product_id=4, quantity=2, price=339000, discount=15),  # Áo sơ mi họa tiết
            OrderDetails(order_id=4, product_id=5, quantity=1, price=399000, discount=20),  # Quần jeans xanh
            OrderDetails(order_id=4, product_id=13, quantity=4, price=919000, discount=10),  # Giày thể thao đen
            OrderDetails(order_id=5, product_id=9, quantity=2, price=80000, discount=20),  # Áo khoác bomber
            OrderDetails(order_id=5, product_id=16, quantity=3, price=299000, discount=5),  # Kính mát thời trang
            OrderDetails(order_id=6, product_id=10, quantity=1, price=749000, discount=5),  # Áo khoác denim
            OrderDetails(order_id=6, product_id=11, quantity=1, price=669000, discount=15),  # Áo khoác hoodie
            OrderDetails(order_id=7, product_id=21, quantity=1, price=309000, discount=10),  # Áo sơ mi caro
            OrderDetails(order_id=7, product_id=19, quantity=2, price=299000, discount=20),  # Túi đeo thời trang Oupica
            OrderDetails(order_id=8, product_id=18, quantity=2, price=299000, discount=20),  # Kính mát Leyean
            OrderDetails(order_id=8, product_id=15, quantity=1, price=199000, discount=15),  # Thắt lưng da
            OrderDetails(order_id=9, product_id=12, quantity=1, price=669000, discount=10),  # Giày thể thao hồng
            OrderDetails(order_id=9, product_id=20, quantity=2, price=299000, discount=5),  # Đồng hồ nam Pasika
            OrderDetails(order_id=10, product_id=21, quantity=3, price=309000, discount=20),  # Áo sơ mi caro
            OrderDetails(order_id=10, product_id=17, quantity=1, price=149000, discount=10),  # Mũ lưỡi trai
            OrderDetails(order_id=11, product_id=11, quantity=2, price=669000, discount=15),  # Áo khoác hoodie
            OrderDetails(order_id=11, product_id=5, quantity=1, price=399000, discount=25),  # Quần jeans xanh
            OrderDetails(order_id=12, product_id=12, quantity=8, price=799000, discount=30),  # Áo khoác da
            OrderDetails(order_id=12, product_id=16, quantity=3, price=299000, discount=20)  # Kính mát phong cách

        ]
        db.session.add_all(order_details_data)
        db.session.commit()

        data_mes = [
            Messages(buyer_id=4, content="Chào bạn, tôi có thể hỏi về sản phẩm này không?"),
            Messages(buyer_id=4, content="Sản phẩm này có sẵn màu nào vậy?", serder=True),
            Messages(buyer_id=4, content="Giá sản phẩm này có thể thương lượng không?", serder=True),
            Messages(buyer_id=4, content="Thời gian giao hàng mất bao lâu?"),
            Messages(buyer_id=4, content="Sản phẩm này có bảo hành không?"),
            Messages(buyer_id=4, content="Có thể gửi thêm hình ảnh của sản phẩm không?", serder=True),
            Messages(buyer_id=4, content="Kích thước của sản phẩm này là gì?"),
            Messages(buyer_id=4, content="Có thể đổi trả sản phẩm nếu không vừa không?", serder=True),
            Messages(buyer_id=4, content="Sản phẩm này có thể sử dụng cho những mục đích nào?"),
            Messages(buyer_id=4, content="Bạn có thể cho tôi biết thêm về chính sách giao hàng không?", serder=True)
        ]
        db.session.add_all(data_mes)
        db.session.commit()

        feedback_data=[
            FeedbackProduct(user_id=4,product_id=1, comment="Tối quá", rating=4),
            FeedbackProduct(user_id=4, product_id=1, comment="Oke quá", rating=3),
        ]
        db.session.add_all(feedback_data)
        db.session.commit()


