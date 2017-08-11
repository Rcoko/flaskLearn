#!/usr/bin/env python
# -- coding: utf-8 --
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from urllib import quote
from pyquery import PyQuery as pq
from selenium import webdriver

class ReqWebInfo(object):
    @staticmethod
    def get_wx_article_info(wx_url):
        browser = webdriver.PhantomJS()
        browser.get(wx_url)
        html = browser.execute_script("return document.documentElement.outerHTML")
        return html

