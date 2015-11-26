#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
1. 用于查看GI日志是否存在可能的丢额；
2. 如果gi上的日志没有查出丢额，用于查看丢额的用户通过哪个web登陆的。
'''
import sys, os

log_dir = '/opt/tomcat-7.0/logs'
log_error = 'error_log.txt'
log_name_list = []

#get the correct log names 
def estimate_log(log_name):
    for line in gi_log_list:
        if log_name == line.split('/')[4].replace('\n', ''):
            log_name_list.append(log_name)
            break
    else:
        print '\033[0;32;40m%s 是错误的GI日志文件。\033[0m' % log_name

#get the information of the users who may lost their account.
def get_info(log_name):
    print '\033[0;32;40m-\033[0m'*15 + '\033[0;32;40m%s\033[0m' % log_name + '\033[0;32;40m-\033[0m'*15 
    os.system('cat %s/%s |grep "network error" |grep billno= |awk \'{print $1,$2","$0}\' |awk -F"," \'{print $1,$3,$5,$6,$7,$8}\' > %s/%s' %(log_dir, log_name, log_dir, log_error))
    os.system('cat %s/%s' %(log_dir, log_error))

#if sys.argv[2] and sys.argv[3] do not exist, then exit.
def not_exist():
    global user_name
    global user_bilno
    try:
        user_name = sys.argv[2]
    except:
        print '\033[0;36;40m缺少用户账号。\033[0m'
        sys.exit(0)
    try:
        user_bilno = sys.argv[3]
    except:
        print '\033[0;36;40m缺少关联提案号。\033[0m'
        sys.exit(0)

#help for the script.
def help_doc(log_name_in):
    if log_name_in == '-h' or log_name_in == '--help':
        print "\033[0;32;40m介绍：用于查看GI日志是否存在可能的丢额，如果需要查看丢额的用户是过哪个web登陆的，则提供[用户名] [关联提案号]\033[0m"
        print '\033[0;32;40m用法: ./get_weburl.py "日志名1 日志名2" [用户名] [关联提案号]\033[0m'
        sys.exit(0)
    else:
        pass

#if the user_name does not in the log_error, then get the web_url
def get_web_url(log_name):
    print '\033[0;32;40m-\033[0m'*15 + '\033[0;32;40m%s\033[0m' % log_name + '\033[0;32;40m-\033[0m'*15 
    os.system('cat %s/%s |grep "network error" |grep billno= |awk \'{print $1,$2","$0}\' |awk -F"," \'{print $1,$3,$5,$6,$7,$8}\' > %s/%s' %(log_dir, log_name, log_dir, log_error))
    with open('%s/%s' %(log_dir, log_error), 'r') as log_read:
        error_list = log_read.readlines()
    for line in error_list:
        if user_name in line:
            print "\033[0;36;40m%s 的丢额在GI日志中:\033[0m" % user_name
            print line
            #break
    else:
        get_time_list = os.popen('cat %s/%s |grep %s |grep %s |awk -F":" \'{print $1":"$2}\' | tail -1' %(log_dir, log_name, user_name, user_bilno)).readlines()
        #print get_time_list
        if len(get_time_list) == 0:
            print "\033[0;36;40m%s 在此日志中没发现此关联提案号(%s)的丢额。\033[0m" %(user_name, user_bilno)
        else:
            time_str = get_time_list[0].replace('\n', '')
            web_url_list = ['ag6.net\n', 'ag6.com\n', 'ag8.com\n', 'ag9.com\n', 'www.ag6.net\n', 'www.ag6.com\n', 'www.ag8.com\n', 'www.ag9.com\n']
            web_url_log_list = os.popen('cat %s/%s |grep "%s" |grep "%s"|awk -F"/" \'{print $3}\'' %(log_dir, log_name, user_name, time_str)).readlines()
            for web_url in web_url_list:
                if web_url in web_url_log_list:
                    print "\033[0;36;40m%s 的丢额没在GI日志中:\033[0m" % user_name
                    print "\033[0;35;40m%s %s 是从 %s 上进入游戏的。\033[0m" %(time_str, user_name, web_url.replace('\n', ''))
                    break
            else:
                print "\033[0;31;40m%s:没有找到web登陆记录，请手动查询。\033[0m" % user_name
#main of the script
if __name__ == "__main__":
    #if sys.argv[1] does not exist, then exit.
    try:
        global log_name_in
        log_name_in = sys.argv[1]
    except:
        print '请输入正确的GI日志文件。'
        sys.exit(0)

    #get the names of GI logs
    gi_log_list = os.popen('ls %s/* |grep "catalina.out"' % log_dir).readlines()

    #introduce
    help_doc(log_name_in)

    #get the correct log
    for log_name in log_name_in.split(' '):
        estimate_log(log_name)

    #if no input log name is correct, then exit.
    if log_name_list == []:
        sys.exit(0)

    print "\033[0;33;40m以下为出现 network error 可能丢额的用户:\033[0m"
    #get the information of the users who may lost their account.
    for log_name in log_name_list:
        get_info(log_name)
    print '\033[0;32;40m-\033[0m'*20 + '\033[0;32;40m分界线\033[0m' + '\033[0;32;40m-\033[0m'*20

    #if sys.argv[2] and sys.argv[3] do not exist, then exit.
    not_exist()

    #if the user_name does not in the log_error, then get the web_url
    for log_name in log_name_list:
        get_web_url(log_name)
    print '\033[0;32;40m-\033[0m'*20 + '\033[0;32;40m分界线\033[0m' + '\033[0;32;40m-\033[0m'*20
