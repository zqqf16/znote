#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import define, options

import os

from handler import admin, frontend, article, category

define("port", default=8888, help="run on the given port", type=int)

class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            # Admin
            (r'/admin[/]?', admin.AdminHandler),

            (r'/admin/article[/]?', article.ShowHandler),
            (r'/admin/article/write[/]?', article.WriteHandler),
            (r'/admin/article/action[/]?', article.ActionHandler),

            (r'/admin/category[/]?', category.ShowHandler),
            (r'/admin/category/add[/]?', category.AddHandler),
            (r'/admin/category/delete[/]?', category.DeleteHandler),

            (r'/login[/]?', admin.LoginHandler),

            # Frontend
            (r'/', frontend.IndexHandler),
            (r'/article/([0-9]+).html', frontend.SingleHandler),
            (r'/comment[/]?', frontend.CommentHandler),
            (r'/([^/]+)[/]?', frontend.SlugHandler),
            (r'.*', frontend.PageNotFoundHandler),
        ]

        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "login_url": "/login",
            "cookie_secret": "ZmViNDQ4OTk5NmU4NDVlNGRhMGJhNmFiODA3OGRjNDFjOTQzYzZhNgo=",
        }

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
