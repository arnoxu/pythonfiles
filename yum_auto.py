#!/usr/bin/env python
#-_- coding:utf-8 -_-
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.files import *


#set the hosts
env.roledefs = {
    "tomcat_server":['192.168.254.109', '192.168.254.110', '192.168.254.111'],
    "new":['192.168.254.112']
}
env.user = 'root'
env.port = '22'
env.password = 'pythonon'

yum_path = '/etc/yum.repos.d'
yum_file = 'localyum.repo'

#env.exclude_hosts = 

def mkdir_mount():
#    with settings(warn_only = True):
#        exist_d = run("ls /mnt/* |grep redhat")
    with cd('/'):
        if exists('/mnt/redhat6.0'):
            pass
        else:       
            run('mkdir /mnt/redhat6.0')

def put_yum():
    with cd("%s" %yum_path):
        if exists('%s' % yum_file):
            pass
        else:
            put('%s/%s' %(yum_path, yum_file), '%s/' % yum_path)

def mount():
    mount = run("mount |grep redhat")
    if mount == "":
        run("mount /dev/cdrom /mnt/redhat6.0")
    else:
        pass

def auto_mount():
    auto_mount = local("cat /etc/rc.local |grep redhat", capture=True)
    with settings(warn_only=True):
        auto_conf = run("cat /etc/rc.local |grep redhat")
        if auto_conf == "":
            run("echo %s >> /etc/rc.local")
        else:
            pass

@runs_once
def deploy():
    execute(mkdir_mount)
    execute(put_yum)
    execute(mount)
    execute(auto_mount)


#def test_yum():
#    with prefix("yum clean all"):
#        run("yum search httpd")
    
#def mount_auto():
#    run("echo 'mount /dev/sr0 /mnt/redhat6.0' >> /etc/rc.local")
  

#for update files
def update_files():
#"""用于同步/arno/tomcat6.0 和/usr/local/apr"""
    with cd(""):
        if exists("/arno/tomcat6.0"):
            pass
        else:
            run("mkdir -p /arno/tomcat6.0")
        if exists("/usr/local/apr"):
            pass
        else:
            run("mkdir -p /usr/local/apr")
    put("/arno/tomcat6.0/*", "/arno/tomcat6.0/")
    put("/usr/local/apr/*","/usr/local/apr")
    run("rm -rf /arno/tomcat6.0/tomcat6.0 /usr/local/apr/apr")

def update_profile():
    run("rm -rf /etc/profile")
    put("/etc/profile","/etc/profile")
    run(". /etc/profile")


def update_jdk():
    put("/usr/java","/usr/")


def auto_tomcat():
    put("/etc/init.d/tomcatd", "/etc/init.d/")
    run("chkconfig --add tomcatd")



