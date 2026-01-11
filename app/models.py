from sqlalchemy import Column, Integer, String ,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="articles")

    tags = relationship(
        "Tag",
        secondary="article_tags",
        back_populates="articles"
    )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    articles = relationship("Article", back_populates="owner")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    articles = relationship(
        "Article",
        secondary="article_tags",
        back_populates="tags"
    )


class ArticleTag(Base):
    __tablename__ = "article_tags"
    
    article_id = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)