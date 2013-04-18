#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import tornado.web
import module 

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, **kargs):
        self.db = module.get_session()

    def get_current_user(self):
        uid = self.get_secure_cookie('user')
        if not uid:
            return None
        
        user = self.db.query(module.User).get(uid)
        return user

    def get_template_namespace(self):
        # Add 'api' to template namespace
        namespace = tornado.web.RequestHandler.get_template_namespace(self)
        namespace.update(api = module.QueryAPI(self.db))
        return namespace
