#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
add_big_customers.py - 用于添加大客户
'''

from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import exists,contains

#定义工作目录和脚本名称
shell_dir = '/home/tomcat'
shell_name = 'check.sh'
shell_gi = 'check-gi.sh'
shell_gc = 'check-gc.sh'

#定义主机
env.roledefs = {
    'ONE':['192.168.100.56', '192.168.100.57', '192.168.100.71'],
    'TWO':['202.55.16.115'],
}

env.user = 'tomcat'
env.port = '2862'

HK = ['192.168.100.56', '192.168.100.57', '192.168.100.71']
Amazon = []
Eastern = []

#判断主机使用的登陆KEY
def _check_host():
    if env.host in HK:
        env.key_filename = '/opt/fab/KEYS/hk_server'
        env.password = '5FIq24TaAVA7tMjHAW4K'
    elif env.host in Amazon:
        env.key_filename = '/opt/fab/KEYS/amazon_server'
    elif env.host in Eastern:
        env.key_filename = '/opt/fab/KEYS/eastern_server' 
    else:
        env.password = 'ygGP2&huhytAqza!NwJR'

#添加大客户
@roles('ONE')
def _add_ONE(big_cut):
    ''' big_cut = 账号:姓名 '''
    env.exclude_hosts = ['192.168.100.57']
    _check_host()
    with cd('%s' % shell_dir):
        if contains('%s' % shell_name, big_cut):
            print green("大客户 %s 已经存在。" % big_cut)
        else:
            run ('sed -i \'s/=(/=(%s /\' %s ' % (big_cut, shell_name))
            if contains('%s' % shell_name, big_cut):
                print green("大客户添加成功。")
            else:
                print red("大客户添加失败。")

@roles('TWO')
def _add_TWO(big_cut):
    ''' big_cut = 账号:姓名 '''
    _check_host()
    with cd('%s' % shell_dir):
        if contains('%s' % shell_gi, big_cut):
            print green("大客户 %s 已经存在脚本 %s 中。" % (big_cut, shell_gi))
        else:
            run ('sed -i \'s/=(/=(%s /\' %s ' % (big_cut, shell_gi))
            if contains('%s' % shell_gi, big_cut):
                print green("大客户添加成功。")
            else:
                print red("大客户添加失败。")
        if contains('%s' % shell_gc, big_cut):
            print green("大客户 %s 已经存在脚本 %s 中。" % (big_cut, shell_gc))
        else:
            run ('sed -i \'s/=(/=(%s /\' %s ' % (big_cut, shell_gc))
            if contains('%s' % shell_gc, big_cut):
                print green("大客户添加成功。")
            else:
                print red("大客户添加失败。")

#删除大客户
@roles('ONE')
def _delete_ONE(big_cut):
    ''' big_cut = 账号:姓名 '''
    env.exclude_hosts = ['192.168.100.57']
    _check_host()
    with cd('%s' % shell_dir):
        if not contains('%s' % shell_name, big_cut):
            print green("大客户 %s 不存在。" % big_cut)
        else:
            run ('sed -i \'s/%s //\' %s ' % (big_cut, shell_name))
            if not contains('%s' % shell_name, big_cut):
                print green("大客户删除成功。")
            else:
                print red("大客户删除失败。")

@roles('TWO')
def _delete_TWO(big_cut):
    ''' big_cut = 账号:姓名 '''
    _check_host()
    with cd('%s' % shell_dir):
        if not contains('%s' % shell_gi, big_cut):
            print green("大客户 %s 不存在脚本 %s 中。" % (big_cut, shell_gi))
        else:
            run ('sed -i \'s/%s //\' %s ' % (big_cut, shell_gi))
            if not contains('%s' % shell_gi, big_cut):
                print green("大客户删除成功。")
            else:
                print red("大客户删除失败。")
        if not contains('%s' % shell_gc, big_cut):
            print green("大客户 %s 不存在脚本 %s 中。" % (big_cut, shell_gc))
        else:
            run ('sed -i \'s/%s //\' %s ' % (big_cut, shell_gc))
            if not contains('%s' % shell_gc, big_cut):
                print green("大客户删除成功。")
            else:
                print red("大客户删除失败。")


#执行
@task
def add(big_cut):
    '''用法： add:账号:姓名'''
    execute(_add_ONE, big_cut)
    execute(_add_TWO, big_cut)

@task
def delete(big_cut):
    '''用法： delete:账号:姓名'''
    execute(_delete_ONE, big_cut)
    execute(_delete_TWO, big_cut)
