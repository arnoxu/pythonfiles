#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
python crawler -- download pintures from baidu tieba.
'''

import re
import urllib

#get html
def _get_html(url):
	page = urllib.urlopen(url)
	html = page.read(page)
	return html
	
#set baidu tieba url and get data of the website
url = 'http://tieba.baidu.com/p/4115907322'
html = _get_html(url)
#print html

#download pictures
def _get_img(html):
	reg = r'src="(http://.+?\.jpg)"'
	imgre = re.compile(reg)
	imglist = re.findall(imgre, html)
	print imglist
	for i, imgurl in enumerate(imglist):
		urllib.urlretrieve(imgurl, '/arno/pictures/%s.jpg' % i)
	
_get_img(html)
