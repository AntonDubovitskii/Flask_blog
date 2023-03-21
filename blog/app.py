import os

from combojsonapi.spec import ApiSpecPlugin
from flask import Flask

from blog.admin import admin
from blog.models import User
from blog.security import flask_bcrypt
from blog.views.articles import articles_app
from blog.extensions import db, login_manager, migrate, api
from blog.views.authors import authors_app


def create_app() -> Flask:
    app = Flask(__name__)

    cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"
    app.config.from_object(f"blog.configs.{cfg_name}")

    register_blueprints(app)
    register_extensions(app)
    register_api_routes()

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    flask_bcrypt.init_app(app)
    admin.init_app(app)

    api.plugins = [
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


def register_api_routes():
    from blog.api.tag import TagList, TagDetail
    from blog.api.user import UserList, UserDetail
    from blog.api.author import AuthorList, AuthorDetail
    from blog.api.article import ArticleList, ArticleDetail

    api.route(TagList, "tag_list", "/api/tags", tag="Tag")
    api.route(TagDetail, "tag_detail", "/api/tags/<int:id>/", tag="Tag")

    api.route(UserList, "user_list", "/api/users/", tag="User")
    api.route(UserDetail, "user_detail", "/api/users/<int:id>/", tag="User")

    api.route(AuthorList, "author_list", "/api/authors/", tag="Author")
    api.route(AuthorDetail, "author_detail", "/api/authors/<int:id>/", tag="Author")

    api.route(ArticleList, 'article_list', '/api/articles/', tag='Article')
    api.route(ArticleDetail, 'article_detail', '/api/articles/<int:id>', tag='Article')


def register_blueprints(app: Flask):
    from blog.views.auth import auth_app
    from blog.views.users import users_app

    app.register_blueprint(users_app, url_prefix="/users")
    app.register_blueprint(articles_app, url_prefix="/articles")
    app.register_blueprint(auth_app, url_prefix="/auth")
    app.register_blueprint(authors_app, url_prefix="/authors")






