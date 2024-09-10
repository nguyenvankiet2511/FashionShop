from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask import redirect, request, url_for
from flask_login import logout_user, current_user
from AppShop import admin, db, app
from AppShop.models import UsersRole, Accounts, Products, Categories, BillingAddress


# class AuthenticatedModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.users_role_id == UsersRole.ADMIN
# View để xử lý việc đăng xuất
class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect(url_for('show_login'))
class StatusView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect(url_for('show_login'))

# View để quản lý Products
class ProductsView(ModelView):
    column_list = ['id', 'name', 'price', 'category_id', 'unitsInStock', 'discount', 'createdDate', 'updatedDate']
    form_columns = ['name', 'price', 'description', 'imageProduct', 'category_id', 'unitsInStock', 'discount']

class CategoriesView(ModelView):
    column_list = ['id', 'name']
    column_labels = {
        'id': 'Mã danh mục',
        'name': 'Tên danh mục'
    }

# Thêm các view vào Flask-Admin
admin.add_view(CategoriesView(Categories,db.session,name='Danh mục'))
admin.add_view(ProductsView(Products,db.session,name='Sản phẩm'))
admin.add_view(StatusView(name="Thống kê"))
admin.add_view(LogoutView(name="Đăng xuất"))
