from datetime import datetime
from os import abort

from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask import redirect, request, url_for
from flask_login import logout_user, current_user
from AppShop import admin, db, app, dao
from AppShop.models import UsersRole, Accounts, Products, Categories, BillingAddress
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField



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
    @expose("/", methods=['POST', 'GET'])
    def index(self):
        rel = request.form.get('rel')
        if rel:
            year = int(rel.split('-')[0])
            month = int(rel.split('-')[1])
        else:
            current_date = datetime.now()
            year = current_date.year
            month = current_date.month

        listOrder = dao.get_order_details_with_info()
        totalYear = dao.get_revenue_by_year(year)
        revenue_month_current = dao.get_revenue_by_month_current(month=month, year=year)
        totalItems = dao.get_total_items_sold_by_year(year)
        totalItemsMonth= dao.get_total_items_sold_by_month(month,year)
        revenue_by_quarter = dao.get_revenue_by_quarter(year)
        revenueThreeYear = dao.get_revenue_last_3_years()
        bestSeller = dao.get_best_selling_product_by_year(year)
        bestSellerMonth = dao.get_best_selling_product_month(month, year)
        revenueProduct = dao.doanh_thu_san_pham_theo_thang_nam(month, year)
        tonKho = dao.tong_ton_kho()
        danh_muc_mua = dao.tong_so_luong_mua_theo_danh_muc(month, year)
        doanhthuDM = dao.doanh_thu_theo_danh_muc(month, year)
        return self.render('admin/status.html',totalItemsMonth=totalItemsMonth,bestSellerMonth=bestSellerMonth,
                           revenue_month_current=revenue_month_current, doanhThuDM=doanhthuDM, xxx=danh_muc_mua,
                           tonKho=tonKho, revenueProduct=revenueProduct,
                           bestSeller=bestSeller, revenueThreeYear=revenueThreeYear, year=year, month=month,
                           orders=listOrder,
                           totalYear=totalYear, totalItems=totalItems, revenueQuarter=revenue_by_quarter)


# View để quản lý Products


class ProductsView(ModelView):
    # Danh sách các cột hiển thị trong bảng
    column_list = [
        'id',
        'name',
        'price',
        'category_id',
        'unitsInStock',
        'discount',
        'createdDate',
        'updatedDate'
    ]



class CategoriesView(ModelView):
    column_list = ['id', 'name']
    column_labels = {
        'id': 'Mã danh mục',
        'name': 'Tên danh mục'
    }
    column_filters = ['name']


class AccountsView(ModelView):
    # Danh sách các cột hiển thị trong bảng
    column_list = ['id', 'name', 'email', 'username', 'active', 'users_role_id']

    # Các trường xuất hiện trong form thêm mới và chỉnh sửa
    form_columns = ['name', 'email', 'username', 'password', 'active', 'users_role_id']

    # Tùy chỉnh nhãn cột
    column_labels = {
        'id': 'Mã tài khoản',
        'name': 'Tên',
        'email': 'Email',
        'username': 'Tên người dùng',
        'active': 'Trạng thái',
        'users_role_id': 'Vai trò người dùng'
    }
    column_exclude_list = ['password']
    def on_model_change(self, form, model, is_created):
        if is_created or form.password.data:
            model.set_password(form.password.data)
    def is_accessible(self):
        return True
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            abort(403)  # Chặn truy cập nếu không có quyền



# Thêm các view vào Flask-Admin
admin.add_view(CategoriesView(Categories, db.session, name='Danh mục'))
admin.add_view(ProductsView(Products, db.session, name='Sản phẩm'))
admin.add_view(AccountsView(Accounts,db.session, name="Tài khoản"))
admin.add_view(StatusView(name="Thống kê"))
admin.add_view(LogoutView(name="Đăng xuất"))


