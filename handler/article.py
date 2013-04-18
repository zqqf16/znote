#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from tornado.escape import json_encode
from datetime import datetime

from module import Article
from base import BaseHandler

class ArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        category = self.get_argument('c', default='all')
        status = self.get_argument('s', default='all')
        order_by = self.get_argument('o', default='default')

        result = self.db.query(Article)

        if category != 'all':
            c_id = None if category == 'none' else category
            result = result.filter(Article.category_id == c_id)

        if status != 'all':
            result = result.filter(Article.status == status)

        if order_by != 'default':
            order = {
                'create': Article.created.desc(),
                'modify': Article.modified.desc(),
                'view': Article.view_count.desc(),
            }

            if order_by in order:
                result = result.order_by(order[order_by])

        self.render('admin.html', articles=result.all(), 
            category=category, status=status, order_by=order_by)

class WriteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id', default=None)
        article = self.db.query(Article).get(id) if id else None
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
            article = self.db.query(Article).get(aid)
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
            article = Article(title=title, 
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
        status = self.get_argument('status', default=None)
        aid = self.get_argument('id', default=None)

        if not action or not aid:
            self.write(u'''{"status": 1, "msg": "参数错误"}''')
            return

        article = self.db.query(Article).get(article_id)
        if not article:
            self.write(u'''{"status": 2, "msg": "文章没找到"}''')

        if action == 'published' or action == 'draft' or action == 'page':
            article.status = action
        elif action == 'delete':
            self.db.delete(article)

        self.db.commit()
        self.write('''{"status": 0}''')
