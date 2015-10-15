# encoding=utf8

from base import BaseHandler
from utils.decorators import render_to
from tornado.web import url


class IndexHandler(BaseHandler):

    @render_to
    def get(self):
        return 'index.html', locals()

url_list = (
    url(r"/?", IndexHandler),
)
