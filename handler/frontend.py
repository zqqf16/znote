#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from module import * 
from base import Base

theme_page = 'theme/new/'

# For frontend
class PageNotFound(Base):
    '''404 error page'''
    def get(self):
        self.render(theme_page+'404.html')
    def post(self):
        self.render(theme_page+'404.html')
        
class Index(Base):
    '''Index page'''
    def get(self):
        ctg = self.get_argument('c', default=None)
        articles = self.db.query(Article).filter(Article.status=='published')
        if ctg == '0':
            articles = articles.filter(Article.category_id == None)
        elif ctg:
            articles = articles.filter(Article.category_id == ctg)

        self.render(theme_page+'index.html', articles=articles.order_by(Article.created.desc()).all())

class Comment(Base):
    def post(self):
        aid = self.get_argument("article", default=None)
        name = self.get_argument("name", default=None)
        url = self.get_argument("url", default=None)
        email = self.get_argument("emain", default=None)
        content = self.get_argument("content", default=None)

        redirect = self.request.headers['Referer']

        if not name or not content:
            self.redirect(redirect)

        article = self.db.query(Article).get(aid)
        if not article:
            self.redirect(redirect)

        comment = Comment(
            username = name,
            url = url,
            email = email,
            content = content,
            article = article,
        )

        self.db.add(comment)
        self.db.commit()
        self.redirect(redirect)

class Single(Base):
    '''Single article page'''
    def get(self, aid):
        article = self.db.query(Article).get(aid)
        if not article: 
            raise tornado.web.HTTPError(404)

        #increase the view_count
        article.view_count += 1
        self.db.commit()

        self.render(theme_page+'single.html', article=article)

class Slug(Base):
    def get(self, slug):
        article = self.db.query(Article).filter(Article.slug==slug).first()
        if not article: 
            raise tornado.web.HTTPError(404)

        #increase the view_count
        article.view_count += 1
        self.db.commit()

        self.render(theme_page+'single.html', article=article)
