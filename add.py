#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
add_big_customers.py - 用于添加/删除大客户
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
    'BAK':['192.168.100.56'],
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
    elif env.host in Amazon:
        env.key_filename = '/opt/fab/KEYS/amazon_server'
    elif env.host in Eastern:
        env.key_filename = '/opt/fab/KEYS/eastern_server' 
    else:
        pass
#判断本地大客户脚本是否与远程服务器的一致
#如果不一致则进行更新
@runs_once
def _get_shell():
    with lcd(local_dir):
        local('rm -rf %s.bak' % shell_name)
        get('%s/%s' %(shell_dir, shell_name), '%s/%s.bak' %(local_dir, shell_name))
        with settings(warn_only = 1):
            result = local('diff %s %s.bak' %(shell_name, shell_name), capture = True)
        if result == '':
            pass
        else:
            local('rm -rf %s %s %s' %(shell_name, shell_gi, shell_gc))
            local('cp %s.bak %s' %(shell_name, shell_name))
            local('cp %s.bak %s' %(shell_name, shell_gi))
            local('cp %s.bak %s' %(shell_name, shell_gc))

#获取脚本中的大客户名单
def _get_cut(shell_name):
    with open('%s/%s' %(local_dir, shell_name), 'r') as f_shell:
        shell_list = f_shell.readlines()
    for line in shell_list:
        if 'username=(' in line:
            big_cut_name = line
            break
    return big_cut_name


#判断脚本，并添加删除指定大客户。
except_list = ['', ' ', '\t', '\r', '\n', '\\t', '\\r', '\\n']

def _contains_add(shell_name, big_cut):
    with settings(warn_only = True):
        big_cut_list = big_cut.split(' ')
        big_cut_name = _get_cut(shell_name)
        for big_cut_i in big_cut_list:
            big_cut_e = big_cut_i.replace('/', '\/')
            if big_cut_e in except_list:
                continue
            elif big_cut_i not in big_cut_name:
                local ('sed -i \'/username=(/s/=(/=(%s /\' %s ' % (big_cut_e, shell_name))
                big_cut_name = _get_cut(shell_name)
                if big_cut_i not in big_cut_name:
                    print red("大客户添加失败，请检查脚本。")
                else:
                    print yellow("大客户 %s 添加成功。" % big_cut_i)
            else:
                print yellow("大客户 %s 已经存在脚本 %s 中" % (big_cut_i, shell_name))

def _contains_delete(shell_name, big_cut):
    with settings(warn_only = True):
        big_cut_list = big_cut.split(' ')
        big_cut_name = _get_cut(shell_name)
        for big_cut_i in big_cut_list:
            big_cut_e = big_cut_i.replace('/', '\/')
            if big_cut_e in except_list:
                continue
            elif big_cut_i not in big_cut_name:
                print yellow("需要删除的大客户 %s 不在脚本 %s 中" % (big_cut_i, shell_name))
            else:
                local ('sed -i \'/username=(/s/%s //g\' %s ' % (big_cut_e, shell_name))
                big_cut_name = _get_cut(shell_name)
                if big_cut_i not in big_cut_name:
                    print yellow("大客户 %s 删除成功。" % big_cut_i)
                else:
                    print red("大客户 %s 删除失败，请检查脚本。" % big_cut_i)

#添加大客户
@runs_once
def _add_local(big_cut):
    with lcd('%s' % local_dir):
        print cyan("------------------------%s------------------------" % shell_name)
        _contains_add(shell_name,big_cut)
        print cyan("------------------------%s------------------------" % shell_gi)
        _contains_add(shell_gi,big_cut)
        print cyan("------------------------%s------------------------" % shell_gc)
        _contains_add(shell_gc,big_cut)
        print cyan("--------------------------------------------------------")

#删除大客户
@runs_once
def _delete_local(big_cut):
    with lcd('%s' % local_dir):
        print cyan("------------------------%s------------------------" % shell_name)
        _contains_delete(shell_name,big_cut)
        print cyan("------------------------%s------------------------" % shell_gi)
        _contains_delete(shell_gi,big_cut)
        print cyan("------------------------%s------------------------" % shell_gc)
        _contains_delete(shell_gc,big_cut)
        print cyan("-------------------------------------------------------")

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

#commit git, 提交脚本修改到git版本库
def _commit_git(commit_log, big_cut):
    commit_log_in = commit_log + big_cut
    with lcd(local_dir):
        try:    
            local('git add *')
            local("git commit -m ''' %s '''" % commit_log_in)
        except:
            print red('脚本没有被修改，请确认大客户是否添加/删除成功。')

#执行
@task
@roles('ONE')
@runs_once
def add(big_cut):
    '''用法： add:"账号:姓名 账号:姓名"'''
    execute(_check_host)
    execute(_get_shell)
    execute(_add_local, big_cut)
    execute(_commit_git, "添加大客户：", big_cut)
    execute(_decide)

@task
@roles('ONE')
@runs_once
def delete(big_cut):
    '''用法： delete:"账号:姓名 账号:姓名"'''
    execute(_check_host)
    execute(_get_shell)
    execute(_delete_local, big_cut)
    execute(_commit_git, "删除大客户：", big_cut)
    execute(_decide)

@task
def update():
    '''更新大客户脚本到远程服务器。'''
    with lcd(local_dir):
        commit_log_in = "手动更新大客户脚本到远程服务器"
        try:    
            local('git add ../*')
            local("git commit -m ''' %s '''" % commit_log_in)
            execute(_put_ONE)
            execute(_put_TWO)
        except:
            result = confirm(green("大客户脚本没有修改，请确认是否更新到远程服务器："))
            if result:
                execute(_put_ONE)
                execute(_put_TWO)
            else:
                print red("更新大客户脚本到远程服务器失败。")

##获取脚本   
#@task
#def _get_shell():
#    _check_host()
#    get('%s/%s' % (shell_dir, shell_name), '%s' % local_dir)
