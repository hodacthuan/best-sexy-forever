import redis
from . import constants

pool = redis.ConnectionPool(
    host=constants.REDISDB_SERVER,
    port=constants.REDISDB_PORT,
    db=constants.REDISDB_DBNUMBER,
    password=constants.REDISDB_PASSWORD
)

redisClient = redis.Redis(connection_pool=pool)

ttl = {
    'day': 86400,
    'h6': 21600,
    'm10': 600,
    'h1': 3600,
    'h3': 10800
}

key1 = {
    'request': 'request:',
    'response': 'response:',
    'database': 'database:',
    'ip': 'ip:',
}

key2 = {
    'album': 'album:',
    'tag': 'tag:',
    'category': 'category:',
}

key3 = {
    'hotgirlbiz': 'hotgirlbiz:',
    'kissgoddess': 'kissgoddess:',
}


def get(key):
    return redisClient.get(key).decode('utf-8')


def set(key, value):
    return redisClient.set(key, value.encode('utf-8'))


def setex(key, value, ttl):
    return redisClient.set(key, value.encode('utf-8'), ttl)
