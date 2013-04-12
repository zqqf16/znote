#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import tornado.web
from tornado.escape import json_encode
from datetime import datetime
from module import * 
from api import *

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, **kargs):
        self.db = get_session()
        self.api = ModuleAPI(self.db)

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        
        user = self.db.query(User).get(user_id)
        return user

class PageNotFoundHandler(BaseHandler):
    def get(self):
        self.render("404.html")
    def post(self):
        self.render("404.html")
        
class IndexHandler(BaseHandler):
    def get(self):
        articles = self.db.query(Article).filter(Article.status=='publish').all()
        self.render("index.html", articles=articles, api=self.api)

class SingleHandler(BaseHandler):
    def get(self, article_id):
        article = self.db.query(Article).get(article_id)
        if not article: 
            raise tornado.web.HTTPError(404)
        article.view_count += 1
        self.db.commit()
        self.render("single.html", article=article, api=self.api)

class PageHandler(BaseHandler):
    def get(self, article_slug):
        article = self.db.query(Article).filter(Article.slug==article_slug).first()
        if not article: 
            raise tornado.web.HTTPError(404)
        self.render("page.html", article=article, api=self.api)


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
            return

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
        category = self.get_argument("category", default="all")
        status = self.get_argument("status", default="all")
        order_by = self.get_argument("order_by", default="default")

        result = self.db.query(Article)
        if category != "all":
            c_id = None if category == 'none' else category
            result = result.filter(Article.category_id == c_id)
        if status != "all":
            result = result.filter(Article.status == status)
        if order_by != "default":
            order = {
                'create': Article.created.desc(),
                'modify': Article.modified.desc(),
                'view': Article.view_count.desc(),
            }
            result = result.order_by(order[order_by])

        self.render("admin.html", articles=result.all(), api=self.api, 
            category=category, status=status, order_by=order_by)

class WriteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", default=None)
        if id:
            article = self.db.query(Article).get(id)
        else:
            article = None
        self.render("write.html", article=article, api=self.api)
    
    @tornado.web.authenticated
    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        
        title = self.get_argument("title", default=None)
        content = self.get_argument("content", default=None)
        id = self.get_argument("id", default=0)
        status = self.get_argument("status", default="publish")
        slug = self.get_argument("slug", default=None)
        category_id = self.get_argument("category", default=None)

        rst = {}
            
        if id != 0:
            article = self.db.query(Article).get(id)
            article.title = title
            article.content = content
            article.status = status
            article.author_id = self.current_user.id
            article.slug = slug
            article.modified = datetime.now()
            article.category_id = category_id

        else:
            article = Article(title=title, 
                              content=content,
                              status=status,
                              slug=slug,
                              author_id=self.current_user.id,
                             )
            self.db.add(article)

        self.db.commit()
        rst['status'] = 0
        rst['article'] = {'id': article.id}
        self.write(json_encode(rst))

class ArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        action = self.get_argument("action", default=None)
        article_id = self.get_argument("id", default=None)
        if not action or not article_id \
                or action not in ("delete", "publish", "draft", "fix"):
            self.write(json_encode({"status": 1, "msg": "error"}))
            return

        article = self.db.query(Article).get(article_id)
        if not article:
            self.write(json_encode({"status": 2, "msg": "not found"}))

        if action == "publish" or action == "draft":
            article.status = action
        elif action == "fix":
            article.status = "page"
        elif action == "delete":
            self.db.delete(article)

        self.db.commit()
        self.write(json_encode({"status": 0}))

class PageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pages = self.db.query(Article).filter(Article.status=="page").all()
        self.render("admin_page.html", pages=pages, api=self.api)

class CategoryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("category.html")

    @tornado.web.authenticated
    def post(self):
        action = self.get_argument("action", default=None)
        name = self.get_argument("name", default=None)
        cid = self.get_argument("id", default=None)

        if action not in ("add", "edit", "delete"):
            self.write(json_encode({"status": 1, "msg": "error"}))
            return

        if action == "add":
            if not name:
                self.write(json_encode({"status": 1, "msg": "error"}))
                return
            ctg = self.db.query(Category).filter(Category.name == name)
            if ctg:
                self.write(json_encode({"status": 2, "msg": "already exist"}))
                return
            else:
                ctg = Category(name=name)
                self.db.add(ctg)
                self.db.commit()
                self.write(json_encode({"status": 0, "category": ctg.id}))
                return
        elif action == "edit":
            if not name or not cid:
                self.write(json_encode({"status": 1, "msg": "error"}))
                return
            ctg = self.db.query(Category).get(cid)
            if not ctg:
                self.write(json_encode({"status": 3, "msg": "not found"}))
                return
            
            ctg.name = name
            self.db.commit()
            self.write(json_encode({"status": 1}))
            return

        elif action == "delete":
            if not cid:
                self.write(json_encode({"status": 1, "msg": "error"}))
            
            ctg = self.db.query(Category).get(cid)
            if not ctg:
                self.write(json_encode({"status": 3, "msg": "not found"}))
                return
            
            self.db.delete(ctg)
            self.db.commit()
            self.write(json_encode({"status": 1}))
            return
