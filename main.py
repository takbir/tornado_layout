# encoding=utf8

import os
import sys
import logging

import settings
import urls

import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado.options import define, parse_command_line


define('log_file_prefix', default=os.path.join(settings.SITE_ROOT, 'logs', 'access.log'))
define('log_rotate_mode', default='time')
define('log_rotate_when', default='D')
define('log_rotate_interval', default=1)
parse_command_line()

logger = logging.getLogger(__file__)


class PageNotFoundHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("error.html")

    def post(self):
        self.render("error.html")

    def initialize(self, status_code):
        self.set_status(status_code)


if len(sys.argv) > 1:
    MAIN_SITE_PORT = int(sys.argv[1])
else:
    MAIN_SITE_PORT = settings.SITE_PORT

tornado.web.ErrorHandler = PageNotFoundHandler

if __name__ == "__main__":

    # i18n
    # tornado.locale.load_translations(settings.settings['translations'])
    application = urls.application

    # bind signals
    sockets = bind_sockets(MAIN_SITE_PORT)

    if not settings.DEBUG and settings.OS == 'linux':
        import tornado.process
        tornado.process.fork_processes(0)  # 0 表示按 CPU 数目创建相应数目的子进程

    server = HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    logger.info(settings.SITE_URL)
    tornado.ioloop.IOLoop.instance().start()
