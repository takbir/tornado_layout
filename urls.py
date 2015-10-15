# encoding=utf8

import tornado.web
import settings
from common.importlib import import_module

url_mapping = [
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler,
     {"path": "%s/static" % settings.SITE_ROOT}),
]

"""
url 的映射分散到各个模块中的py文件里, 这里不再集中存放.

usage:

from tornado.web import url

...

url_list = (
    url(r"/?", IndexHandler),
    )

然后在下面的_views中定义需要载入的模块名称

"""

_views = (
    'index.v_index',
)


def load_urls():
    url_list = []
    # 扫描所有views
    for _view in _views:
        module = import_module(_view)
        if hasattr(module, 'url_list'):
            urls = module.url_list
            url_list.extend(urls)
    return url_list

url_mapping.extend(load_urls())

application = tornado.web.Application(url_mapping, **settings.settings)
