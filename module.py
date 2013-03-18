#!/usr/bin/env python
# -*- coding: utf-8 -*-

#SQLALchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy import ForeignKey, Table  
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import defer, undefer
#Time
from datetime import datetime
#Markdown2
import markdown2

import db

#--------------------------------
# Database
#--------------------------------
Base = declarative_base()

#--------------------------------
# Tables
#--------------------------------
#users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64)) 
    nickname = Column(String(64))
    password = Column(String(128))
    salt = Column(String(128)) 
    email = Column(String(128))
    last_ip = Column(String(128)) 

article_category = Table('relationships', Base.metadata, 
                         Column('article_id', Integer, ForeignKey('articles.id')), 
                         Column('category_id', Integer, ForeignKey('categories.id'))
                        )

#articles
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum('published','draft'), default='published')
    slug = Column(String(128), default=None)
    view_count = Column(Integer, default=0)
    #relationship
    author = relationship('User', backref=backref('articles', lazy='dynamic'))
    categories = relationship('Category', 
                            secondary=article_category, 
                            passive_deletes=True, 
                            backref=backref('articles', lazy='dynamic')
                           )

    @hybrid_property
    def markdown(self):
        return markdown2.markdown(self.content)

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


if __name__ == '__main__':
    import hashlib

    db.init_db(Base)
    session = db.get_session()

    #Don't forget to change it!
    username = 'zqqf16'
    pwd = hashlib.md5('123456').hexdigest()
    salt = hashlib.md5(datetime.now().ctime()).hexdigest()
    pwd = hashlib.md5(pwd+salt).hexdigest()
    user = User(username=username, password=pwd, nickname="Zorro", email='zqqf16@gmail.com')
    session.add(user)

    article = Article(title=u'Hello World', content=u'这是一篇默认文章', author=user)
    catg = Category(name=u'测试')
    article.categories.append(catg)
    session.add(article)
    session.commit()
