# encoding=utf8

import redis
import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_ADDRESS, port=settings.REDIS_PORT, db=2)


def get_redis_conn():
    return redis.Redis(connection_pool=pool)


def redis_set(key, value, time=None):
    con = get_redis_conn()
    result = None
    if time:
        result = con.set(key, value)
        con.expire(key, time)
    else:
        result = con.set(key, value)
    return result


def redis_get(key):
    con = get_redis_conn()
    return con.get(key)


def redis_delete(key):
    con = get_redis_conn()
    con.delete(key)


class RedisQueue(object):

    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.__db = get_redis_conn()
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.
        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)
