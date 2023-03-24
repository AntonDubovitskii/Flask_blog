import os

from combojsonapi.permission import PermissionPlugin
from combojsonapi.spec import ApiSpecPlugin
from combojsonapi.event import EventPlugin
from flask import Flask

from blog.admin import admin
from blog.models import User
from blog.security import flask_bcrypt
from blog.extensions import db, login_manager, migrate, api, csrf


def create_app() -> Flask:
    app = Flask(__name__)

    cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"
    app.config.from_object(f"blog.configs.{cfg_name}")

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    flask_bcrypt.init_app(app)
    admin.init_app(app)

    api.plugins = [
        EventPlugin(),
        PermissionPlugin(strict=False),
        ApiSpecPlugin(
            app=app,
            tags={
                'Tag': 'Tag API',
                'User': 'User API',
                'Author': 'Author API',
                'Article': 'Article API',
            }
        ),
    ]
    api.init_app(app)

    login_manager.login_view = "auth_app.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).one_or_none()


def register_blueprints(app: Flask):
    from blog.views.auth import auth_app
    from blog.views.users import users_app
    from blog.views.authors import authors_app
    from blog.views.articles import articles_app
    from blog.api.views import api_blueprint

    app.register_blueprint(users_app, url_prefix="/users")
    app.register_blueprint(articles_app, url_prefix="/articles")
    app.register_blueprint(auth_app, url_prefix="/auth")
    app.register_blueprint(authors_app, url_prefix="/authors")
    app.register_blueprint(api_blueprint)






