#!/usr/bin/env python
# -*- coding: utf-8 -*-

#SQLALchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy import ForeignKey, Table, or_  
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Time
from datetime import datetime
#Markdown2
import markdown2

#--------------------------------
# Database
#--------------------------------
Base = declarative_base()
engine = create_engine('sqlite:///znote.db', echo=False)

def init_db():
    Base.metadata.create_all(engine)

def get_session():
    return sessionmaker(bind=engine)()

#--------------------------------
# Tables
#--------------------------------
#users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False) 
    nickname = Column(String(64))
    password = Column(String(128), nullable=False)
    salt = Column(String(128), nullable=False) 
    email = Column(String(128))
    last_ip = Column(String(128)) 

#articles
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum('published','draft','page'), default='published')
    slug = Column(String(128), default=None)
    view_count = Column(Integer, default=0)
    comment_status = Column(Enum('allow', 'forbid'), default='allow')
    #relationship
    author = relationship('User', backref=backref('articles'))
    category = relationship('Category', backref=backref('articles'))

    @hybrid_property
    def markdown(self):
        return markdown2.markdown(self.content)

#categories
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
 
#configurations
class Config(Base):
    __tablename__ = 'configurations'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    value = Column(String(256), nullable=False)

#comments
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    email = Column(String(128))
    url = Column(String(128))
    content = Column(Text, default=None)

    article_id = Column(Integer, ForeignKey('articles.id'))
    parent_id = Column(Integer, ForeignKey('comments.id'))

    children = relationship('Comment')
    article = relationship('Article', backref=backref('comments', lazy='dynamic'))

# Links
class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    url = Column(String(128), nullable=False)
    title = Column(String(128), nullable=False)

# Api
class QueryAPI():
    def __init__(self, session):
        self.session = session

    def get_articles(self, type='published'):
        return self.session.query(Article).filter(Article.status==type).all()

    def get_article_by_id(self, article_id):
        return self.session.query(Article).get(article_id)

    def get_article_by_slug(self, article_slug):
        return self.session.query(Article).filter(Article.slug==article_slug).first()

    def get_categories(self):
        return self.session.query(Category).all()

    def get_category_by_id(self, category_id):
        return self.session.query(Category).get(category_id)

    def get_category_by_name(self, category_name):
        return self.session.query(Category).filter(Category.name==category_name).first()

if __name__ == '__main__':
    import hashlib

    init_db()
    session = get_session()

    #Don't forget to change it!
    username = 'zqqf16'
    pwd = hashlib.md5('123456').hexdigest()
    salt = hashlib.md5(datetime.now().ctime()).hexdigest()
    pwd = hashlib.md5(pwd+salt).hexdigest()
    user = User(username=username, password=pwd, salt=salt, nickname="Zorro", email='zqqf16@gmail.com')
    session.add(user)

    article = Article(title=u'Hello World', content=u'这是一篇默认文章', author=user)
    c = Comment(username="zorro", url="www.baidu.com", email="zqqf16.gmail.com", content=u'测试')
    catg = Category(name=u'测试')
    article.category = catg
    article.comments.append(c)
    session.add(article)
    session.commit()
