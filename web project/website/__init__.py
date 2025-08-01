from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import render_template

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'NLICWEB'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asset_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    from .models import User

    login_manager.login_view = 'auth.login'  
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import models
    with app.app_context():
        db.create_all() 

    from .views import views
    from .auth import auth
    from .admin import admin
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    return app
