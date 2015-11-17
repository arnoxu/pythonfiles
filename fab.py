#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
learn the fabric function
'''
from fabric.contrib import console
from fabric.api import *

def _confirm():
    answer_in = console.confirm('Do you wish to continue:')
    if answer_in == True:
        print "You wish to continue. Your answer is %s" % answer_in
    else:
        print "You wish to abort."

#local文件的内容的判断
def _contains(shell_name, big_cut):
    with settings(warn_only = True):
        big_cut_d = local('echo %s |sed \'s/ /, /g\'' % big_cut, capture = True)
        
        result = local('cat %s |egrep "%s"' % (shell_name, big_cut_d), capture = True)
    if result.failed:
        return False
    else:
        return True

def deploy():
    execute(_confirm)


