#!/usr/bin/env python
#-_- python: utf-8 -_-
'''
test.py - practise to use python crawler
'''

import urllib

#get datas from web url
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

url = 'http://gc.agg028.com/agingame2/images/ad/goodroad_loading_hw_zh.jpg'

html = getHtml(url)























##test variable in function
##variables in function can not be used as global variables.
#def func_va():
#    test_va = 100
#    print test_va
#func_va()
#print test_va



