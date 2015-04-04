#encoding=utf8

import time
from common.log_utils import getLogger
log = getLogger('memorize_cache.py')

__all__ = ['memorize', 'memcache_client']

import memcache
import settings
memcache_client = memcache.Client(settings.settings['memcache_server'])

OBJ_DICT = {}
OBJ_DICT2 = {}
OBJ_EXPIRE_DICT = {}
OBJ_EXPIRE_DICT2 = {}
DEFAULT_EXPIRE_SECONDS = 60*30
DEFAULT_VERSION_EXPIRE_SECONDS = 60*60*24*30
MEMORY_CLEANER_PERIOD = 60*30
OBJ_VERSION_DICT = {}

def set_remote_obj_version(key, version):
    return memcache_client.set(key, version, DEFAULT_VERSION_EXPIRE_SECONDS)

def get_remote_obj_version(key):
    return memcache_client.get(key) or 0

def set_local_obj_version(key, version):
    OBJ_VERSION_DICT[key] = version

def get_local_obj_version(key):
    return OBJ_VERSION_DICT.get(key) or 0

def version_expired(key):
    local_version = get_local_obj_version(key)
    remote_version = get_remote_obj_version(key)
    return local_version != remote_version

def arg_to_str(obj):
    import mongoengine.base
    cls_valid = isinstance(obj, mongoengine.base.metaclasses.TopLevelDocumentMetaclass)
    if cls_valid:
        return str('clz_%s' % obj.__name__)
    return str(obj)

def start_memory_cleaner():
    while True:
        time.sleep(MEMORY_CLEANER_PERIOD)
        keys_to_remove = []
        for key, value in OBJ_EXPIRE_DICT.iteritems():
            if OBJ_EXPIRE_DICT[key] < int(round(time.time())):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            try:
                del OBJ_DICT[key]
                del OBJ_EXPIRE_DICT[key]
                del OBJ_VERSION_DICT[key]
            except KeyError:
                pass
        keys_to_remove = []
        for key, value in OBJ_EXPIRE_DICT2.iteritems():
            if OBJ_EXPIRE_DICT2[key] < int(round(time.time())):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            try:
                del OBJ_DICT[key]
                del OBJ_EXPIRE_DICT2[key]
                del OBJ_VERSION_DICT[key]
            except KeyError:
                pass

memory_cleaner_thread_started = False
def start_memory_cleaner_thread():
    global memory_cleaner_thread_started
    import threading
    if not memory_cleaner_thread_started:
        threading.Thread(target=start_memory_cleaner, args=(), name='memory_cleaner_thread').start()
        memory_cleaner_thread_started = True

def memorize(function):
    """内存缓存, 用于不定参数的函数
    Usage:
        def xxx(key1,key2,refresh=False)
            return instance
        def xxx(key1,key2,key2,x1=xx,x2=yyy)
            return instance
    """
    def helper(*args, **kwargs):
        refresh = False
        expire = None
        if kwargs.has_key('refresh'):
            refresh = kwargs['refresh']
        if kwargs.has_key('expire'):
            expire = kwargs['expire']
        args_str = map(arg_to_str, args)
        key = '%s#%s' % (function.__name__, '#'.join(args_str))
        remote_version = get_remote_obj_version(key)
        ret_obj = None
        if refresh:
            remote_version += 1
            set_remote_obj_version(key, remote_version)
        else:
            if remote_version == 0:
                ret_obj = function(*args, **kwargs)
                OBJ_DICT[key] = ret_obj
                set_remote_obj_version(key, 1)
                set_local_obj_version(key, 1)
            else:
                local_version = get_local_obj_version(key)
                if local_version != remote_version:
                    ret_obj = function(*args, **kwargs)
                    OBJ_DICT[key] = ret_obj
                    set_local_obj_version(key, remote_version)
                    OBJ_EXPIRE_DICT2[key] = int(round(time.time())) + (expire or DEFAULT_EXPIRE_SECONDS)
                else:
                    if key in OBJ_DICT:
                        ret_obj = OBJ_DICT[key]
                    else:
                        ret_obj = function(*args, **kwargs)
                        OBJ_DICT[key] = ret_obj
        return ret_obj
    return helper

@memorize
def test(x):
    return file(x).read()

if __name__ == '__main__':
    x = 'aaa'
    txt = test(x)

    txt = test(x)
