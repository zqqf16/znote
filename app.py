#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import define, options

import os

import db
from handler import *

define("port", default=8888, help="run on the given port", type=int)

class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/login', LoginHandler),
            (r'/admin', AdminHandler),
            (r'/admin/write', WriteHandler),
            (r'/admin/status', StatusHandler),
            (r'/admin/pages', PageHandler),
            (r'/article/([0-9]+).html', SingleHandler),
            (r'/([0-9a-zA-Z_-]+)', PageHandler),
            (r'.*', PageNotFoundHandler),
        ]

        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "login_url": "/login",
            "cookie_secret": "ZmViNDQ4OTk5NmU4NDVlNGRhMGJhNmFiODA3OGRjNDFjOTQzYzZhNgo=",
        }

        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = db.get_session()

if __name__ == '__main__':
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
