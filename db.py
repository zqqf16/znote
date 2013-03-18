#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///zn.db', echo=False)

def init_db(base):
    base.metadata.create_all(engine)

def get_session():
    return sessionmaker(bind=engine)()
