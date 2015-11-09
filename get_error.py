#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
用于查看额度丢失
'''
from fabric.api import *
import sys

env.roledefs = {
    'b79_gi':['tomcat@192.168.100.56:2862'],
#    'b79_gi':['192.168.100.56', '192.168.100.71'],
#    'b79_web':['192.168.100.55', '192.168.100.70', '59.188.133.168'],
}
env.user = 'tomcat'
env.port = '2862'

HK = ['192.168.100.56', '192.168.100.71', '192.168.100.55', '192.168.100.70']
Eastern = []
Amazon = []

#log dir
log_dir = '/opt/tomcat-7.0/logs'
log_name = 'catalina.out'
log_dir_168 = '/opt/tomcat-7.0_7070_b79_web/logs/'

#check hosts
def _check_host():
    if env.host in HK:
        env.key_filename = ['/arno/KEYS/hk_server']
    elif env.host in Eastern:
        env.key_filename = ['/arno/KEYS/eastern_server']
    elif env.host in Amazon:
        env.key_filename = ['/arno/KEYS/amazon_server']
    else:
        env.key_filename = []

#get gi error log
def _get_gi_error_log():
    log_name_in = sys.stdin.read()
    print log_name_in
    if log_name_in == '':
        with cd('%s' % log_dir):
            run('cat catalina.out |grep "network error" |grep billno= |awk \'{print $1,$2","$0}\' |awk -F"," \'{print $1,$3,$5,$6,$7,$8}\'')
    else:
        with cd('%s' % log_dir):
            run('cat %s |grep "network error" |grep billno= |awk \'{print $1,$2","$0}\' |awk -F"," \'{print $1,$3,$5,$6,$7,$8}\'' % log_name_in)



#获取日志
@roles('b79_gi')
def deploy():
    execute(_check_host)
    execute(_get_gi_error_log)





