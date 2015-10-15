# encoding=utf8

import os
import sys
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.curdir))

from common import redis_utils
import cPickle as pickle


def arg_to_str(obj):
    return str(obj)


def memorize_cache(function):
    """Redis缓存, 用于不定参数的函数
    Usage:
        def xxx(key1,key2,refresh=False)
            return instance
        def xxx(key1,key2,key2,x1=xx,x2=yyy)
            return instance
    """

    def helper(*args, **kwargs):
        redis_conn = redis_utils.get_redis_conn()
        refresh = False
        if 'refresh' in kwargs:
            refresh = kwargs.pop('refresh')
        key = '%s#%s#%s' % (
            function.__module__, function.__name__, '#'.join(map(arg_to_str, args)))
        if refresh:
            redis_conn.delete(key)
        else:
            remote_obj_pickle = redis_conn.get(key)
            if not remote_obj_pickle:
                local_obj = function(*args, **kwargs)
                redis_conn.set(key, pickle.dumps(local_obj))
                redis_conn.expire(key, 60 * 30)
                return local_obj
            return pickle.loads(remote_obj_pickle)

    return helper


@memorize_cache
def test_func(val):
    print 'executing function'
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, val]

if __name__ == '__main__':
    # print test_func(1)
    # test_func(1, refresh=True)
    # print test_func(1)
    # print test_func(1)
    import time
    test_func(1, refresh=True)
    begin = time.time()
    for i in xrange(50000):
        test_func(1)
    end = time.time()
    print begin, end, end - begin
