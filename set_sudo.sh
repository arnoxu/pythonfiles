#!/bin/bash
#introduction: set sudo for tomcat.
#              log sudo for all.

USER=`echo $USER`
SUDOLOG='/var/log/sudo.log'

if [ "$USER" != "root" ];then
    echo "请使用root账户执行该脚本。"
    echo "退出脚本。"
    exit 0
fi

if [ -f "$SUDOLOG" ];then
    echo "sudo.log 日志文件已存在。"
else
    touch $SUDOLOG
fi

sleep 1

if [ ! -f "/etc/sudoers" ];then
    echo "/etc/sudoers 文件不存在，请检查。"
fi

GREP_TOMCAT=$(cat /etc/sudoers |grep "tomcat    ALL")
if [ "$GREP_TOMCAT" != "" ];then
    echo "/etc/sudoers 里面已经配置tomcat权限，请查看。"
else
    sed -i '/root\tALL/ atomcat\tALL=(ALL)\tALL' /etc/sudoers
    GREP_SUDOLOG=$(cat /etc/sudoers |grep "sudo.log")
    if [ "$GREP_SUDOLOG" == "" ];then
        sed -i '/tomcat\tALL/ aDefaults\tlogfile=/var/log/sudo.log' /etc/sudoers
    sed -i '/tomcat\tALL/ aDefaults\t!syslog' /etc/sudoers
    fi
fi

sleep 1


if [ ! -f "/etc/syslog.conf" ];then
    echo "/etc/syslog.conf 文件不存在，请检查。"
    echo "退出脚本。"
    exit 0
fi

GREP_SUDOLOG=$(cat /etc/syslog.conf |grep "sudo.log")    
if [ "$GREP_SUDOLOG" == "" ];then
    echo "local2.debug          /var/log/sudo.log" >> /etc/syslog.conf
    echo "/etc/syslog.conf 配置完成。"
else
    echo "/etc/syslog.conf 中已经配置sudo日志。不放心就检查下。"
fi

sleep 1

if [ -f "/etc/init.d/syslog" ];then
    /etc/init.d/syslog restart
else
    echo "/etc/init.d/syslog 文件不存在，无法重启syslog，请检查。"
fi
