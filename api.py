#!/usr/bin/env python
# -*- coding: utf-8 -*-

from module import * 

class ModuleAPI():
    def __init__(self, db):
        self.db = db

    def get_articles(self, type='published'):
        return self.db.query(Article).filter(Article.status==type).all()

    def get_article_by_id(self, article_id):
        return self.db.query(Article).get(article_id)

    def get_article_by_slug(self, article_slug):
        return self.db.query(Article).filter(Article.slug==article_slug).first()

    def get_categories(self):
        return self.db.query(Category).all()

    def get_category_by_id(self, category_id):
        return self.db.query(Category).get(category_id)

    def get_category_by_name(self, category_name):
        return self.db.query(Category).filter(Category.name==category_name).first()
