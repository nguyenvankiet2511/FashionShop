from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from urllib.parse import quote
from flask_admin import Admin
from google_auth_oauthlib.flow import Flow
import os, pathlib

app=Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app.config["SECRET_KEY"]="hsfjrgfjwnfgwejkfnjwegnwj"
app.secret_key="sacfasfgwgwgwgwgwegehehehehru5hrt"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/CreateApi?charset=utf8mb4" % quote(
    "123456")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
admin = Admin(app=app, name='Cosmic Store', template_mode='bootstrap4')
login = LoginManager(app=app)
ma = Marshmallow(app=app)

client_secrets_file = os.path.join(pathlib.Path(__file__).parent.parent, "oauth_config.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri='http://localhost:5001/callback'
)