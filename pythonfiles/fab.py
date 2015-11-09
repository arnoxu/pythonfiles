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

def deploy():
    execute(_confirm)




