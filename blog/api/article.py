from flask_combo_jsonapi import ResourceDetail, ResourceList

from blog.extensions import db
from blog.permissions.article import UserListPermissionArticle, UserPermissionArticle
from blog.schemas import ArticleSchema
from blog.models import Article
from combojsonapi.event.resource import EventsResource


class ArticleListEvents(EventsResource):
    def event_get_count(self, *args, **kwargs):
        return {"count": Article.query.count()}


class ArticleList(ResourceList):
    events = ArticleListEvents
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
        'permission_get': [UserListPermissionArticle],
    }


class ArticleDetail(ResourceDetail):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
        'permission_get': [UserListPermissionArticle],
        'permission_patch': [UserPermissionArticle],
    }




