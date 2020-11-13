import mongoengine


class AccessLogsModel(mongoengine.Document):
    objects = mongoengine.QuerySetManager()

    session_key = mongoengine.StringField()
    path = mongoengine.StringField()
    method = mongoengine.StringField()
    data = mongoengine.DynamicField()
    ipAddress = mongoengine.StringField()
    referrer = mongoengine.StringField()
    timestamp = mongoengine.DateTimeField()

    meta = {'collection': 'accessLogs', 'strict': False}


class Status(mongoengine.Document):
    objects = mongoengine.QuerySetManager()

    hotgirlbizPage = mongoengine.IntField()

    meta = {'collection': 'status', 'strict': False}
