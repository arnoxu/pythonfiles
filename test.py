#!/usr/bin/env python
#-_- coding: utf-8 -_-
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
