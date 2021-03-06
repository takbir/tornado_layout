# encoding=utf8

import os
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_PORT = 80
SITE_DOMAIN = '127.0.0.1'
DOMAIN_PORT = SITE_PORT

OS = 'windows'

DEBUG = True

SECRET_KEY = '1f906fb1638ebdb01ade5f1cb5ljsdhd92e09fcc'

# redis
REDIS_ADDRESS = '127.0.0.1'
REDIS_PORT = 6379

try:
    from local_settings import *
except ImportError:
    print 'load local settings faild.'

if DOMAIN_PORT == 80:
    SITE_URL = 'http://%s' % SITE_DOMAIN
else:
    SITE_URL = 'http://%s:%s' % (SITE_DOMAIN, DOMAIN_PORT)

settings = dict(
    cookie_secret=SECRET_KEY,
    login_url="/login/",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    root_path=os.path.join(os.path.dirname(__file__)),
    xsrf_cookies=True,
    autoescape="xhtml_escape",
    debug=DEBUG,
    xheaders=True,
    # translations=os.path.join(os.path.dirname(__file__), "translations"),  # i18n需要
    # static_url_prefix='', #启用CDN后可修改此定义, 例如: "http://cdn.abc.com/static/"
)
