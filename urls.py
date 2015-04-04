#encoding=utf8

import tornado.web
import settings
from index.v_index import IndexHandler

application = tornado.web.Application([
        (r"/?", IndexHandler),
    ], **settings.settings)
