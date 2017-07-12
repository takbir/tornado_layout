# encoding=utf8

from hashlib import sha1
import os
import time
import datetime

import cache


session_id = lambda: sha1('%s%s' % (os.urandom(16), time.time())).hexdigest()
cache_conn = cache.get_conn()
_skip = (
    '_handler',
    'session_lifetime',
    '_id',
)


class SessionHandler(object):

    def __init__(self, handler, session_lifetime=60 * 60 * 24):
        self._handler = handler
        self.session_lifetime = session_lifetime
        self.init_session()

    def init_session(self):
        """初始化"""
        _id = self._handler.get_secure_cookie("ldsid")
        if not _id:
            _id = session_id()
            cache_conn.hset(_id, 'created', datetime.datetime.now())
        else:
            if not cache_conn.exists(_id):
                _id = session_id()
                cache_conn.hset(_id, 'created', datetime.datetime.now())
        self._handler.set_secure_cookie("ldsid", _id)
        self._id = _id

    def clear(self):
        cache_conn.delete(self._id)

    def __getattr__(self, name):
        if name in _skip:
            return object.__getattr__(self, name)
        cache_conn.expire(self._id, self.session_lifetime)
        return cache_conn.hget(self._id, name)

    def __setattr__(self, name, value):
        if name in _skip:
            object.__setattr__(self, name, value)
        else:
            self.init_session()
            cache_conn.hset(self._id, name, value)
            cache_conn.expire(self._id, self.session_lifetime)

    def __delattr__(self, name):
        if name in _skip:
            object.__delattr__(self, name)
        else:
            cache_conn.hdel(self._id, name)


__all__ = ["SessionHandler", "session_id"]
