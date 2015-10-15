# encoding=utf8

import tornado.web
import tornado.escape
from tornado import locale
import traceback
import settings
from common.session import SessionHandler
import base64
import json


from common.log_utils import getLogger
log = getLogger('base.py')


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session = SessionHandler(self)

    def save_error_msg(self, err_msg):
        pass

    def check_xsrf_cookie(self):
        return True

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
                m_info = 'URL: ' + self.request.host + \
                    self.request.uri + '<br>' + m_info
                # ip = self.request.headers.get("X-Real-Ip", self.request.headers.get("X-Forwarded-For", self.request.remote_ip))
                # m_info_all = 'Ip: ' + ip + '<br>' + m_info
                # err_msg=dict(errcode=str(status_code), content = m_info_all, ip = ip)
                # self.save_error_msg('', err_msg)
                self.render("500.html")
                return
            self.render("error.html", msg=status_code)

    def get_template_namespace(self):
        namespace = super(BaseHandler, self).get_template_namespace()
        namespace['session'] = self.session
        namespace['escape'] = tornado.escape
        namespace['json'] = json
        return namespace

    def get_current_user(self):
        user_id = self.session.user_id
        username = self.session.username
        if not user_id or not username:
            return None
        return dict(
            id=user_id,
            name=username
        )

    def get_params(self):
        encode_params = self.get_argument('s')
        params = base64.b64decode(encode_params)
        return json.loads(params)
