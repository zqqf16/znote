#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import define, options

import os

from handler import admin, frontend

define("port", default=8888, help="run on the given port", type=int)

class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            # Admin
            (r'/admin[/]?', admin.Admin),
            (r'/admin/article[/]?', admin.Article),
            (r'/admin/article/write[/]?', admin.ArticleWrite),
            (r'/admin/article/option[/]?', admin.ArticleOption),
            (r'/login[/]?', admin.Login),

            # Frontend
            (r'/', frontend.Index),
            (r'/article/([0-9]+).html', frontend.Single),
            (r'/comment[/]?', frontend.Comment),
            (r'/([^/]+)[/]?', frontend.Slug),
            (r'.*', frontend.PageNotFound),
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
