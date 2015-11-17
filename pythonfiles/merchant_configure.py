#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
merchant_configure.py - 用于商户部署
'''
import os, sys
import time

#定义工作目录和所需的文件
nginx_conf_dir = '/usr/local/nginx/conf/vhosts'
nginx_conf_module = 'config.conf'
web_conf = 'config.php'
merchant_file = '/home/tomcat/merchant_file.txt'
mysql_passwd = 'ag866.com'
log_file = '/home/tomcat/log.txt'

#读取商户域名和工程
def _get_merchant_info():
    if os.path.exists(merchant_file):
        f_file = file(merchant_file, 'r')
        merchant_list = f_file.readlines()
        return merchant_list
    else:
        return False

#配置商户nginx配置文件以及工程目录
def _merchant_conf():
    if _get_merchant_info() == False:
        print "\033[0;33;40mmerchant_file.txt文件不存在。\033[0m"
        sys.exit()
    else:
        merchant_list = _get_merchant_info()
    print "需要配置的商户列表如下："
    os.system('echo "需要配置的商户列表如下：" >> %s' % log_file)
    for merchant_info in merchant_list:
        print merchant_info,
        os.system('echo "%s" >> %s' %(merchant_info.replace('\n', ''), log_file))
    time.sleep(2)
    count_n = 0
    for merchant_f in merchant_list:
        merchant_www = merchant_f.strip().split(' ')[0]
        merchant_project = merchant_f.strip().replace('\n', '').split(' ')[-1]
        if os.path.exists('/web/%s' % merchant_project):
            pass
        else:
            print "\033[0;33;40m\"%s\": %s 工程文件不存在，请重新上传。\033[0m" %(merchant_www, merchant_project)
            os.system('echo "\"%s\": %s 工程文件不存在，请重新上传。" >> %s' %(merchant_www, merchant_project, log_file))
            count_n += 1
    if count_n > 0: 
        print "退出脚本。"       
        sys.exit()
    for merchant_f in merchant_list:
        merchant_www = merchant_f.strip().split(' ')[0]
        merchant_com = merchant_www.replace('www.', '')
        merchant_project = merchant_f.strip().replace('\n', '').split(' ')[-1]
        print "\n\033[0;36;40m开始配置: \"%s\" \033[0m\n" % merchant_www
        time.sleep(1)
        if os.path.exists('%s/%s.conf' %(nginx_conf_dir, merchant_www)):
            os.system('rm -rf %s/%s.conf' %(nginx_conf_dir, merchant_www))
            os.system('cd %s && cp %s %s.conf' %(nginx_conf_dir, nginx_conf_module, merchant_www))
            os.system('sed -i \'/server_name/s/;/%s %s;/\' %s/%s.conf' %(merchant_www, merchant_com, nginx_conf_dir, merchant_www))
            os.system('sed -i \'/web\//s/web\//web\/%s/\' %s/%s.conf' % (merchant_www, nginx_conf_dir, merchant_www))
        else:
            os.system('cd %s && cp %s %s.conf' %(nginx_conf_dir, nginx_conf_module, merchant_www))
            os.system('sed -i \'/server_name/s/;/%s %s;/\' %s/%s.conf' %(merchant_www, merchant_com, nginx_conf_dir, merchant_www))
            os.system('sed -i \'/web\//s/web\//web\/%s/\' %s/%s.conf' % (merchant_www, nginx_conf_dir, merchant_www))
        if os.path.exists('/web/%s' % merchant_www):
            os.system('rm -rf /web/%s' % merchant_www)
            os.system('mkdir /web/%s' %(merchant_www))
            os.system('cd /web && unrar x %s %s' %(merchant_project, merchant_www))
        else:
            os.system('mkdir /web/%s' %(merchant_www))
            os.system('cd /web && unrar x %s %s' %(merchant_project, merchant_www))
        if os.path.exists('/web/%s/robots.txt' % merchant_www):
            os.system('echo "User-agent: *\nDisallow: /" > /web/%s/robots.txt' % merchant_www)
        else:
            os.system('touch /web/%s/robots.txt' % merchant_www)
            os.system('echo "User-agent: *\nDisallow: /" > /web/%s/robots.txt' % merchant_www)
        os.system('chown nobody.nobody -R /web/%s' % merchant_www)
    os.system('echo "\"%s\": nginx配置完成，web工程配置完成。" >> %s' %(merchant_www, log_file))

#配置数据库
def _set_mysql():
    merchant_list = _get_merchant_info()
    for merchant_f in merchant_list:
        merchant_www = merchant_f.strip().split(' ')[0]
        merchant_name = merchant_www.split('.')[1]
        os.system('mysql -u root -p%s -e "create USER \'%s\'@\'localhost\' IDENTIFIED by \'ag866.com\'"' % (mysql_passwd, merchant_name))
        os.system('mysql -u root -p%s -e "create database %s"' %(mysql_passwd, merchant_name))
        #print "grant all on %s.* to \'%s\'@\'localhost\' identified by \'%s\'" %(merchant_name, merchant_name, mysql_passwd)
        os.system('mysql -u root -p%s -e "grant all on %s.* to \'%s\'@\'localhost\' identified by \'%s\'"' %(mysql_passwd, merchant_name, merchant_name, mysql_passwd))
        os.system('mysql -u root -p%s -e "flush privileges"' % mysql_passwd)
        os.system('echo "\"%s\": %s 数据库用户已创建，权限已设置。" >> %s' %(merchant_www, merchant_name, log_file))

#配置工程目录配置文件
def _set_config():
    merchant_list = _get_merchant_info()
    for merchant_f in merchant_list:
        merchant_www = merchant_f.strip().split(' ')[0]
        merchant_name = merchant_www.split('.')[1]
        if os.path.exists('/web/%s/data/%s' %(merchant_www, web_conf)):
            os.system('sed -i \'/db_user/s/root/%s/\' /web/%s/data/%s' % (merchant_name, merchant_www, web_conf))
            os.system('sed -i \'/db_pass/s/888888/%s/\' /web/%s/data/%s' % (mysql_passwd, merchant_www, web_conf))
        elif os.path.exists('/web/%s/config/%s' %(merchant_www, web_conf)):
            os.system('sed -i \'/DB_USER/s/root/%s/\' /web/%s/config/%s' % (merchant_name, merchant_www, web_conf))
            os.system('sed -i \'/DB_PASSWORD/s/888888/%s/\' /web/%s/config/%s' % (mysql_passwd, merchant_www, web_conf))
        elif os.path.exists('/web/%s/config.inc.php' % merchant_www):
            os.system('sed -i \'/dbUser/s/root/%s/\' /web/%s/config.inc.php' % (merchant_name, merchant_www))
            os.system('sed -i \'/dbPass/s/888888/%s/\' /web/%s/config.inc.php' % (mysql_passwd, merchant_www))
        else:
            print "\033[1;33;40m\"%s\"工程目录配置文件没找到，请手动修改。\033[0m" % merchant_www
            os.system('echo "\"%s\": 工程目录配置文件配置失败，请手动修改。" >> %s' %(merchant_www, log_file))
        os.system('echo "\"%s\": 工程目录配置文件配置成功。" >> %s' %(merchant_www, log_file))
#执行
def _execute():
    _merchant_conf()
    _set_mysql()
    _set_config()


if __name__ == "__main__":
    _execute()

#if _get_merchant_info() == False:
#    print "\033[0;33;40mmerchant_file.txt文件不存在。\033[0m"
#print "\033[0;32;41mGood!\033[0m"
