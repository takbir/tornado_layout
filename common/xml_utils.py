from lxml import etree
import sys
import urllib2,cookielib

def html2tree(data, encoding='utf-8'):
    parser = etree.HTMLParser(encoding=encoding)
    tree = etree.parse(cStringIO.StringIO(data), parser)
    return tree

def xml2tree(xmlfile):
    parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(file(xmlfile), parser)
    return tree

def mm2dict(mmfile):
    pass