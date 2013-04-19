#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import tornado.web
from tornado.escape import json_encode
from datetime import datetime

import module
from base import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/admin')
        else:
            self.render('admin/login.html', user=None, status=0)

    def post(self):
        username = self.get_argument('username', default=None)
        password = self.get_argument('password', default=None)
        if not username or not password:
            # arguments error
            self.render('admin/login.html', user=username, status=1)
            return

        user = self.db.query(module.User).filter(module.User.username==username).first()
        if not user:
            # not found
            self.render('admin/login.html', user=username, status=2)
            return

        hash = hashlib.md5(password+user.salt).hexdigest()

        if hash == user.password:
            self.set_secure_cookie('user', str(user.id))
            self.redirect(self.get_argument('next', default='/admin'))
            return
        else:
            self.render('admin/login.html', user=username, status=3)

class AdminHandler(BaseHandler):
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

        self.render('admin/admin.html', articles=result.all(), 
            category=category, status=status, order_by=order_by)
