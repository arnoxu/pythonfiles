#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
learn the fabric function
'''
from fabric.contrib import console
from fabric.api import *
from fabric.colors import *

def _confirm():
    answer_in = console.confirm('Do you wish to continue:')
    if answer_in == True:
        print "You wish to continue. Your answer is %s" % answer_in
    else:
        print "You wish to abort."

def _local_contain():
#    result = local('cat test.py |grep python', capture = True)
    if _contains('test.py', 'python'):
        print red('测试成功。')
    else:
        print green('测试失败。')

def _contains(shell_name, big_cut):
    with settings(warn_only = True):
        result = local('cat %s |grep %s' % (shell_name, big_cut), capture = True)
    if result.failed:
        return False
    else:
        return True



def deploy():
#    execute(_confirm)
    execute(_local_contain)



