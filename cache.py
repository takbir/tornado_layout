# encoding=utf8

import cPickle as pickle

import redis
import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_ADDRESS, port=settings.REDIS_PORT, db=2)


def get_conn():
    return redis.Redis(connection_pool=pool)


def memorize(function):
    """Redis缓存, 用于不定参数的函数
    Usage:
        def xxx(key1,key2,refresh=False)
            return instance
        def xxx(key1,key2,key2,x1=xx,x2=yyy)
            return instance
    """

    def helper(*args, **kwargs):
        cache_conn = get_conn()
        refresh = False
        if 'refresh' in kwargs:
            refresh = kwargs.pop('refresh')
        key = '%s#%s#%s' % (
            function.__module__, function.__name__, '#'.join([str(a) for a in args]))
        if refresh:
            cache_conn.delete(key)
        else:
            remote_obj_pickle = cache_conn.get(key)
            if not remote_obj_pickle:
                local_obj = function(*args, **kwargs)
                cache_conn.set(key, pickle.dumps(local_obj))
                cache_conn.expire(key, 60 * 30)
                return local_obj
            return pickle.loads(remote_obj_pickle)

    return helper
