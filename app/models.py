# -- coding: utf-8 --

from . import db
from datetime import datetime

class Detail(db.Document):
    meta = {
        'collection': 'details',
        'ordering': ['-create_at'],
        'strict': False,
    }

    title = db.StringField()  #标题
    keywords = db.StringField()  #关键词列表
    description = db.StringField()  #描述
    body = db.StringField()  #内容


