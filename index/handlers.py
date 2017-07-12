# encoding=utf8

from tornado.web import url

from base import BaseHandler
from decorators import render_to


class IndexHandler(BaseHandler):

    @render_to
    def get(self):
        return 'index/index.html', locals()


url_list = (
    url(r"/?", IndexHandler),
)
