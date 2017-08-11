# -- coding: utf-8 --
from mongoengine import *
from . import db
from datetime import datetime

class Categories(Document):
    name = StringField(max_length=30, required=True)
    artnum = IntField(default=0, required=True)
    date = DateTimeField(default=datetime.now(), required=True)

class  Contents(EmbeddedDocument):
    name = StringField()
    date = DateTimeField(default=datetime.now())

class Detail(db.Document):
    meta = {
        'collection': 'details',
        'ordering': ['-create_at'],
        'strict': False,
    }

    title = db.StringField()  #标题
    keywords = db.StringField()  #关键词列表
    description = db.StringField()  #描述
    #categories = ReferenceField(Categories)  #分类
    contents = EmbeddedDocumentField('Contents')   #内容




