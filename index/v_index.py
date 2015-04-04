#encoding=utf8

from base import BaseHandler
from utils.decorators import render_to


class IndexHandler(BaseHandler):

	@render_to
	def get(self):
		return 'index.html', locals()