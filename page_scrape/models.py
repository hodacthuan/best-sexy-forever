from django.db import models

from mongoengine import *
import datetime
class Choice(EmbeddedDocument):
    choice_text = StringField(max_length=200)
    votes = IntField(default=0)


class Poll(Document):
    question = StringField(max_length=200)
    pub_date = DateTimeField(help_text='date published')
    choices = ListField(EmbeddedDocumentField(Choice))
    

class Post(Document):
    objects = QuerySetManager()
    title = StringField(required=True)
    source = StringField(required=True)
    url = StringField(required=True)
    thumbnail = StringField()
    posted = DateTimeField(default=datetime.datetime.utcnow)
    images = ListField(StringField(max_length=2000))
    store = ListField(StringField(max_length=2000))
    content = StringField()



