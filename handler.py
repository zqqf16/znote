#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import tornado.web
from datetime import datetime
from module import * 

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        
        user = self.db.query(User).get(user_id)
        return user

class IndexHandler(BaseHandler):
    def get(self):
        articles = self.db.query(Article).filter(Article.status=='published').all()
        self.render("index.html", articles=articles)

class SingleHandler(BaseHandler):
    def get(self, article_id):
       article = self.db.query(Article).get(article_id)
       if not article: 
           raise tornado.web.HTTPError(404)
       self.render("single.html", article=article)

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/admin")
        else:
            self.render("login.html", user=None, status=0)

    def post(self):
        username = self.get_argument("username", default=None)
        password = self.get_argument("password", default=None)
        if not username or not password:
            self.render("login.html", user=username, status=1)
            return
        user = self.db.query(User).filter(User.username==username).first()
        if not user:
            self.render("login.html", user=username, status=2)

        hash = hashlib.md5(password+user.salt).hexdigest()

        if hash == user.password:
            self.set_secure_cookie('user', str(user.id))
            self.redirect(self.get_argument("next", default="/admin"))
            return
        else:
            self.render("login.html", user=username, status=3)

class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        articles = self.db.query(Article).all()
        self.render("admin.html", articles=articles)

class WriteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", default=None)
        if id:
            article = self.db.query(Article).get(id)
        else:
            article = None
        self.render("write.html", article=article)
    
    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title", default=None)
        content = self.get_argument("content", default=None)
        id = self.get_argument("id", default=None)
        status = self.get_argument("status", default="published")
            
        if id:
            article = self.db.query(Article).get(id)
            article.title = title
            article.content = content
            article.status = status
            article.author_id = self.current_user.id
            article.modified = datetime.now()

        else:
            article = Article(title=title, 
                              content=content,
                              status=status,
                              author_id=self.current_user.id
                             )
            self.db.add(article)

        self.db.commit()
        self.redirect("/admin")
