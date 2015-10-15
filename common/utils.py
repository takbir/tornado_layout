# encoding=utf8
import hashlib
import shutil
import os
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import qrcode
import tornado.template
from HTMLParser import HTMLParser
import math


def md5(astring):
    return hashlib.md5(astring).hexdigest()

# 为了增强memorize功能，将其独立到memory_cache.py中
# def memorize(f):
#     """内存缓存"""
#     memo = {}
#     def helper(x, refresh=False):
#         if refresh or (x not in memo):
#             memo[x] = f(x)
#         return memo[x]
#     return helper


tmpl_loader = tornado.template.Loader("./templates")


def render_to_string(tmpl_file, **adict):
    return tmpl_loader.load(tmpl_file).generate(**adict)


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def touch_file(file_name):
    if not os.path.exists(file_name):
        file_path = os.path.dirname(file_name)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file(file_name, 'wb').write('')


def cutstring(str='', width=10, charset='unicode', addchar='...', br_num=0, line_num=0):
    oldstr = str
    oldaddchar = addchar
    if br_num != 0:
        str_br = u'<br>'
    if type(oldstr).__name__ != 'unicode':
        try:
            oldstr = oldstr.decode(charset)
        except:
            pass

    if oldaddchar and type(oldaddchar).__name__ != 'unicode':
        oldaddchar = oldaddchar.decode(charset)

    index = 0
    usedwidth = 0
    br_index_list = []
    for i in oldstr:
        if ord(i) < 128:
            usedwidth = usedwidth + 1
            if br_num != 0 and index % br_num == 0 and index != 0:
                br_index_list.append(index)
        else:
            usedwidth = usedwidth + 2
            if br_num != 0 and index % (br_num / 2) == 0 and index != 0:
                br_index_list.append(index)
        if usedwidth > width:
            break
        if usedwidth == width:
            if not addchar:
                pass
            elif index == len(oldstr) - 1:
                pass
            else:
                break
        index = index + 1

    if br_num != 0:
        # 记录取到哪
        str_idx = 0
        line_count = 0
        newstr = u''
        # 循环取每行数据并加上换行
        for idx in br_index_list:
            if line_count == line_num - 1:
                newstr += oldstr[str_idx:idx]
            else:
                newstr += oldstr[str_idx:idx] + str_br
            str_idx = idx
            line_count = line_count + 1
        # 取最后剩余不足一行的部分
        if line_count < line_num:
            # 需要分行
            if len(br_index_list) > 0:
                if br_index_list[0] % br_num == 0:
                    newstr = newstr + oldstr[str_idx:width]
                else:
                    newstr = newstr + oldstr[str_idx:width / 2]
            # 无需分行
            else:
                newstr = oldstr
        # 补上...
        if index < len(oldstr):
            newstr = newstr + oldaddchar
    elif index == len(oldstr):
        newstr = oldstr
    elif index < len(oldstr):
        newstr = oldstr[0:index] + oldaddchar

    if charset != 'unicode':
        try:
            newstr = newstr.encode(charset)
        except:
            pass

    return newstr


def get_matrix_img_by_param(content, img_type='png', box_size=5, border=1, img_name='default'):
    q = qrcode.main.QRCode(box_size=box_size, border=border)
    q.add_data(content)
    m = q.make_image()
    return m._img


def get_matrix_img_stream_by_param(content, img_type='png', box_size=5, border=1):
    img = get_matrix_img_by_param(content, img_type, box_size, border)
    mstream = StringIO.StringIO()
    img.__name__ = "xjxjxj.png"
    img.save(mstream, img_type)
    return mstream


def my_urlencode(astring):
    from urllib import urlencode
    return urlencode({'a': astring})[2:]


def remove_dir(Dir):
    if os.path.isdir(Dir):
        paths = os.listdir(Dir)
        for path in paths:
            filePath = os.path.join(Dir, path)
            if os.path.isfile(filePath):
                try:
                    os.remove(filePath)
                except os.error:
                    pass
            elif os.path.isdir(filePath):
                if filePath[-4:].lower() == ".svn".lower():
                    continue
                shutil.rmtree(filePath, True)
    os.rmdir(Dir)
    return True


def get_random_num(k, n=9):
    import random
    p = []
    y1 = [random.randrange(1, n + 1) for i in range(n)]
    y2 = []
    y2.extend(y1)
    y1.sort()
    for j in range(k):
        temp1 = y1[j]
        temp2 = y2.index(temp1)
        p.append(temp2 + 1)
        y2[temp2] = -1
    return_val = ''
    for num in p:
        return_val = return_val + str(num)
    return return_val


def get_same_part_in_lists(list_obj):
    '''传入一个存放多个数组对象的数据，返回公共部分'''
    if len(list_obj) == 0:
        return
    temp = list_obj[0]
    for i in range(1, len(list_obj)):
        temp = list(set(temp).intersection(set(list_obj[i])))
    return temp


def unescape_params(url):
    from tornado.escape import url_unescape
    url = url_unescape(url)
    args_str = url.split('?')[1]
    valid_args = dict([entry.split('=') for entry in args_str.split('&')])
    return valid_args


units = [u'', u'十', u'百', u'千', u'万', u'十', u'百', u'千', u'亿', u'十', u'百', u'千']
nums = [u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九']


def translate_num_to_hanzi(num):
    num = str(num)
    res = ''
    for p in xrange(len(num) - 1, -1, -1):
        r = int(int(num) / math.pow(10, p))
        res += nums[r % 10] + units[p]
    for (i, j) in [(u'零十', u'零'), (u'零百', u'零'), (u'零千', u'零')]:
        res = res.replace(i, j)

    while res.find(u'零零') != -1:
        res = res.replace(u'零零', u'零')
    for (i, j) in [(u'零万', u'万'), (u'零亿', u'亿')]:
        res = res.replace(i, j)
    res = res.replace(u'亿万', u'亿')
    if res.startswith(u'一十'):
        res = res[1:]
    if res.endswith(u'零'):
        res = res[:-1]
    return unicode(res)


def convert2int(string, default=None):
    try:
        return int(string)
    except Exception as e:
        if default is not None:
            return default
        raise e


if __name__ == '__main__':
    translate_num_to_hanzi(10)
