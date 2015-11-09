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

'''
use fabric to manager the linux servers
'''
from fabric.api import *
from fabric.colors import *

#define the hosts and the 
#env.hosts = ['192.168.254.109', '192.168.254.110', '192.168.254.111']
env.roledefs = {
    'tomcat':['192.168.254.109', '192.168.254.110'],
    'mysql':['192.168.254.111']
}
env.user = 'root'
env.port = 22
env.password = 'pythonon'
#env.exclude_hosts = '192.168.254.111'  #for the hosts exclude

@roles('tomcat')
def uname_hosts():
    local('uname -a')
    run('uname -a')
 
@roles('mysql')
def mysql_install():
    run('yum -y install mysql mysql-devel')
