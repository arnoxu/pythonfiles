#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
add_big_customers.py - 用于添加大客户
'''

from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists,contains

#定义工作目录和脚本名称
local_dir = '/opt/fab/Others/others/check_shell'
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

#判断脚本，并添加删除指定大客户。
def _contains_add(shell_name, big_cut):
    with settings(warn_only = True):
        big_cut_list = big_cut.split(' ')
        for big_cut_e in big_cut_list:
            result = local('cat %s |grep "%s"' % (shell_name, big_cut_e), capture = True)
            if result.failed:
                print red("大客户 %s 不在脚本 %s 中。" % (big_cut_e, shell_name))
                local ('sed -i \'s/=(/=(%s /\' %s ' % (big_cut_e, shell_name))
                result = local('cat %s |grep "%s"' % (shell_name, big_cut_e), capture = True)
                if result.failed:
                    print red("大客户添加失败，请检查脚本。")
                else:
                    print yellow("大客户 %s 添加成功。" % big_cut_e)
            else:
                print yellow("大客户 %s 已经存在脚本 %s 中" % (big_cut_e, shell_name))

def _contains_delete(shell_name, big_cut):
    with settings(warn_only = True):
        big_cut_list = big_cut.split(' ')
        for big_cut_e in big_cut_list:
            result = local('cat %s |grep "%s"' % (shell_name, big_cut_e), capture = True)
            if result.failed:
                print yellow("需要删除的大客户 %s 不在脚本 %s 中" % (big_cut_e, shell_name))
            else:
                print red("大客户 %s 在脚本 %s 中，等待删除。。。" % (big_cut_e, shell_name))
                local ('sed -i \'s/%s //g\' %s ' % (big_cut_e, shell_name))
                result = local('cat %s |grep "%s"' % (shell_name, big_cut_e), capture = True)
                if result.failed:
                    print yellow("大客户 %s 删除成功。" % big_cut_e)
                else:
                    print red("大客户 %s 删除失败，请检查脚本。" % big_cut_e)




#@task
#def test(big_cut):
#    with lcd('%s' % local_dir):
#        _contains(shell_name, big_cut)

#添加大客户
@runs_once
def _add_local(big_cut):
    with lcd('%s' % local_dir):
        print cyan("-------------------------------------------------------")
        _contains_add(shell_name,big_cut)
        print cyan("-------------------------------------------------------")
        _contains_add(shell_gi,big_cut)
        print cyan("-------------------------------------------------------")
        _contains_add(shell_gc,big_cut)
        print cyan("-------------------------------------------------------")

#删除大客户
@runs_once
def _delete_local(big_cut):
    with lcd('%s' % local_dir):
        print cyan("-------------------------------------------------------")
        _contains_delete(shell_name,big_cut)
        print cyan("-------------------------------------------------------")
        _contains_delete(shell_gi,big_cut)
        print cyan("-------------------------------------------------------")
        _contains_delete(shell_gc,big_cut)
        print cyan("-------------------------------------------------------")



'''
    with lcd('%s' % local_dir):
        if _contains(shell_name, big_cut):
            print green("大客户 %s 已经存在脚本 %s 中。" % (big_cut, shell_name))
        else:
            local ('sed -i \'s/=(/=(%s /\' %s ' % (big_cut, shell_name))
            if _contains(shell_name, big_cut):
                print green("大客户添加成功。")
            else:
                print red("大客户添加失败。")
        if _contains(shell_gi, big_cut):
            print green("大客户 %s 已经存在脚本 %s 中。" % (big_cut, shell_gi))
        else:
            local ('sed -i \'s/=(/=(%s /\' %s ' % (big_cut, shell_gi))
            if _contains(shell_gi, big_cut):
                print green("大客户添加成功。")
            else:
                print red("大客户添加失败。")
        if _contains(shell_gc, big_cut):
            print green("大客户 %s 已经存在脚本 %s 中。" % (big_cut, shell_gc))
        else:
            local ('sed -i \'s/=(/=(%s /\' %s ' % (big_cut, shell_gc))
            if _contains(shell_gc, big_cut):
                print green("大客户添加成功。")
            else:
                print red("大客户添加失败。")
    with lcd('%s' % local_dir):
        if not _contains('%s' % shell_name, big_cut):
            print green("大客户 %s 不存在脚本 %s 中。" % (big_cut, shell_name))
        else:
            local ('sed -i \'s/%s //g\' %s ' % (big_cut, shell_name))
            if not _contains('%s' % shell_name, big_cut):
                print green("大客户删除成功。")
            else:
                print red("大客户删除失败。")
        if not _contains('%s' % shell_gi, big_cut):
            print green("大客户 %s 不存在脚本 %s 中。" % (big_cut, shell_gi))
        else:
            local ('sed -i \'s/%s //g\' %s ' % (big_cut, shell_gi))
            if not _contains('%s' % shell_gi, big_cut):
                print green("大客户删除成功。")
            else:
                print red("大客户删除失败。")
        if not _contains('%s' % shell_gc, big_cut):
            print green("大客户 %s 不存在脚本 %s 中。" % (big_cut, shell_gc))
        else:
            local ('sed -i \'s/%s //g\' %s ' % (big_cut, shell_gc))
            if not _contains('%s' % shell_gc, big_cut):
                print green("大客户删除成功。")
            else:
                print red("大客户删除失败。")
'''

#更新脚本到服务器
@roles('ONE')
def _put_ONE():
    _check_host()
    with lcd('%s' % local_dir):
        put ('%s' % shell_name, '%s/%s' % (shell_dir, shell_name))



@roles('TWO')
def _put_TWO():
    _check_host()
    with lcd('%s' % local_dir):
        put ('%s' % shell_gi, '%s/%s' % (shell_dir, shell_gi))
        put ('%s' % shell_gc, '%s/%s' % (shell_dir, shell_gc))

#判断是否上传到服务器
def _decide():
    result = confirm (cyan('是否更新到服务器？'))
    if result == True:
        execute(_put_ONE)
        execute(_put_TWO)
    else:
        print red('更新脚本失败，退出。')
        exit(0)

#执行
@task
@roles('ONE')
@runs_once
def add(big_cut):
    '''用法： add:"账号:姓名 账号:姓名"'''
    execute(_check_host)
    execute(_add_local, big_cut)
    execute(_decide)

@task
@roles('ONE')
@runs_once
def delete(big_cut):
    '''用法： delete:"账号:姓名 账号:姓名"'''
    execute(_check_host)
    execute(_delete_local, big_cut)
    execute(_decide)

@task
def update():
    '''更新脚本到远程服务器。'''
    execute(_put_ONE)
    execute(_put_TWO)

##获取脚本   
#@task
#def _get_shell():
#    _check_host()
#    get('%s/%s' % (shell_dir, shell_name), '%s' % local_dir)
