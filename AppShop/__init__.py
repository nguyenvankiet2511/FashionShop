from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from urllib.parse import quote
from flask_admin import Admin

app=Flask(__name__)
app.config["SECRET_KEY"]="hsfjrgfjwnfgwejkfnjwegnwj"
app.secret_key="sacfasfgwgwgwgwgwegehehehehru5hrt"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/CreateApi?charset=utf8mb4" % quote(
    "Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
admin = Admin(app=app, name='Quản Trị NWA', template_mode='bootstrap4')
login = LoginManager(app=app)
ma = Marshmallow(app=app)