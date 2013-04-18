#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import tornado.web
from tornado.escape import json_encode
from datetime import datetime

import module
from base import Base

class Login(Base):
    def get(self):
        if self.current_user:
            self.redirect('/admin')
        else:
            self.render('login.html', user=None, status=0)

    def post(self):
        username = self.get_argument('username', default=None)
        password = self.get_argument('password', default=None)
        if not username or not password:
            # arguments error
            self.render('login.html', user=username, status=1)
            return

        user = self.db.query(module.User).filter(module.User.username==username).first()
        if not user:
            # not found
            self.render('login.html', user=username, status=2)
            return

        hash = hashlib.md5(password+user.salt).hexdigest()

        if hash == user.password:
            self.set_secure_cookie('user', str(user.id))
            self.redirect(self.get_argument('next', default='/admin'))
            return
        else:
            self.render('login.html', user=username, status=3)

class Admin(Base):
    @tornado.web.authenticated
    def get(self):
        category = self.get_argument('category', default='all')
        status = self.get_argument('status', default='all')
        order_by = self.get_argument('order_by', default='default')

        result = self.db.query(module.Article)

        if category != 'all':
            c_id = None if category == 'none' else category
            result = result.filter(module.Article.category_id == c_id)

        if status != 'all':
            result = result.filter(module.Article.status == status)

        if order_by != 'default':
            order = {
                'create': module.Article.created.desc(),
                'modify': module.Article.modified.desc(),
                'view': module.Article.view_count.desc(),
            }

            if order_by in order:
                result = result.order_by(order[order_by])

        self.render('admin.html', articles=result.all(), 
            category=category, status=status, order_by=order_by)

class ArticleWrite(Base):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id', default=None)
        article = self.db.query(module.Article).get(id) if id else None
        self.render('write.html', article=article)
    
    @tornado.web.authenticated
    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        
        title = self.get_argument('title', default=None)
        content = self.get_argument('content', default=None)
        aid = self.get_argument('id', default='0')
        status = self.get_argument('status', default='published')
        slug = self.get_argument('slug', default=None)
        cid = self.get_argument('category', default=None)

        if not title or not content:
            self.write(u'''{"status": 1, "msg": "标题或者内容不能为空"}''')
            return

        if status not in ('published', 'draft', 'page'):
            self.write(u'''{"status": 1, "msg": "违法的状态"}''')
            return

        if not slug:
            slug = title

        if aid != '0':
            article = self.db.query(module.Article).get(aid)
            if not article:
                self.write(u'''{"status": 2, "msg": "文章没找到"}''')
                return
            article.title = title
            article.content = content
            article.status = status
            article.author_id = self.current_user.id
            article.slug = slug
            article.modified = datetime.now()
            if cid:
                article.category_id = cid

        else:
            article = module.Article(title=title, 
                              content=content,
                              status=status,
                              slug=slug,
                              author_id=self.current_user.id,
                              category_id=cid,
                             )
            self.db.add(article)

        self.db.commit()

        rst = {'status': 0, 'article': {'id': article.id}}
        self.write(json_encode(rst))

class ArticleOption(Base):
    @tornado.web.authenticated
    def post(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        action = self.get_argument('action', default=None)
        article_id = self.get_argument('id', default=None)
        if not action or not article_id \
                or action not in ('delete', 'published', 'draft', 'page'):
            self.write(u'''{"status": 1, "msg": "参数错误"}''')
            return

        article = self.db.query(module.Article).get(article_id)
        if not article:
            self.write(u'''{"status": 2, "msg": "文章没找到"}''')

        if action == 'published' or action == 'draft' or action == 'page':
            article.status = action
        elif action == 'delete':
            self.db.delete(article)

        self.db.commit()
        self.write('''{"status": 0}''')

class Article(Base):
    pass

class Category(Base):
    @tornado.web.authenticated
    def get(self):
        self.render('category.html')

    @tornado.web.authenticated
    def post(self):
        action = self.get_argument('action', default=None)
        name = self.get_argument('name', default=None)
        cid = self.get_argument('id', default=None)

        if action not in ('add', 'edit', 'delete'):
            self.write(json_encode({'status': 1, 'msg': 'error'}))
            return

        if action == 'add':
            if not name:
                self.write(json_encode({'status': 1, 'msg': 'error'}))
                return
            ctg = self.db.query(module.Category).filter(module.Category.name == name)
            if ctg:
                self.write(json_encode({'status': 2, 'msg': 'already exist'}))
                return
            else:
                ctg = module.Category(name=name)
                self.db.add(ctg)
                self.db.commit()
                self.write(json_encode({'status': 0, 'category': ctg.id}))
                return
        elif action == 'edit':
            if not name or not cid:
                self.write(json_encode({'status': 1, 'msg': 'error'}))
                return
            ctg = self.db.query(module.Category).get(cid)
            if not ctg:
                self.write(json_encode({'status': 3, 'msg': 'not found'}))
                return
            
            ctg.name = name
            self.db.commit()
            self.write(json_encode({'status': 1}))
            return

        elif action == 'delete':
            if not cid:
                self.write(json_encode({'status': 1, 'msg': 'error'}))
            
            ctg = self.db.query(module.Category).get(cid)
            if not ctg:
                self.write(json_encode({'status': 3, 'msg': 'not found'}))
                return
            
            self.db.delete(ctg)
            self.db.commit()
            self.write(json_encode({'status': 1}))
            return