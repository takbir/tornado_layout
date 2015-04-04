#encoding=utf8
import tornado.web
import traceback
import settings
from tornado import locale

from common.log_utils import getLogger
log = getLogger('base.py')


class BaseHandler(tornado.web.RequestHandler):

    def save_error_msg(self, err_msg):
        pass

    def get_user_locale(self):
        local_code = self.get_secure_cookie('local_code')
        if not local_code:
            local_code = "zh_CN"
            self.set_secure_cookie('local_code', local_code)
        return locale.get(local_code)

    def write_error(self, status_code, **kwargs):
        if settings.settings.get('debug', False):
            self.set_header('Content-Type', 'text/plain')
            exc_str = traceback.format_exception(*kwargs.get("exc_info"))
            m_info = ''.join(exc_str)
            self.finish(m_info)
        else:
            if status_code == 500:
                exc_str = traceback.format_exception(*kwargs.get("exc_info"))
                m_info = ''.join(exc_str).replace("\n", "<br>")
                m_info = 'URL: ' + self.request.host + self.request.uri + '<br>' + m_info
                ip = self.request.headers.get("X-Real-Ip", self.request.headers.get("X-Forwarded-For", self.request.remote_ip))
                m_info_all = 'Ip: ' + ip + '<br>' + m_info
                err_msg=dict(errcode=str(status_code), content = m_info_all, ip = ip)
                self.save_error_msg('', err_msg)
                self.render("500.html")
                return
            self.render("error.html")
