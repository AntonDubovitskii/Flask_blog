from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from blog.extensions import db
from blog.models.article_tag import article_tag_assosiation_table


class Article(db.Model):
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    title = Column(String(300), unique=True, nullable=False, default="", server_default="")
    body = Column(Text, nullable=False, default="", server_default="")
    dt_created = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    dt_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = relationship("Author", back_populates="articles")
    tags = relationship(
        "Tag",
        secondary=article_tag_assosiation_table,
        back_populates="articles",
    )

    def __repr__(self):
        return f"Article #{self.id} {self.title!r} {self.dt_updated!r}>"

    def __str__(self):
        return self.title
