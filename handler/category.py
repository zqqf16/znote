#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from datetime import datetime

import module
from base import BaseHandler

class ShowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self): 
        self.render('category.html')

class AddHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('name', default=None)
        cid = self.get_argument('id', default='0')

        if not name:
            self.write(self.__result(1, u'参数错误'))
            return

        if cid != '0':
            ctg = self.db.query(module.Category).get(cid)
            if not ctg:
                self.write(self.__result(2, u'分类不存在'))
            ctg.name = name
        else:
            ctg = module.Category(name=name)
            self.db.add(ctg)
            
        self.db.commit()
        self.write(self.__result(0, u'成功'))

class DeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        cid = self.get_argument('id', default='0')

        if cid == '0':
            self.write(self.__result(1, u'参数错误'))
            return

        ctg = self.db.query(module.Category).get(cid)
        if not ctg: 
            self.write(self.__result(2, u'分类不存在'))
            return
            
        self.db.delete(ctg)
        self.db.commit()

        self.write(self.__result(0, u'成功'))
