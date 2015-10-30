#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
use for download some static file
'''

import urllib
import time

TIME_TODAY = time.strftime('%Y%m%d')

url = 'http://gc.agg028.com/agingame2/xml/hosts/B79.xml'

def download_file(url):
    urllib.urlretrieve(url, '/arno/files/B79.%s.xml' % TIME_TODAY)

download_file(url)


