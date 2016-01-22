#!/bin/bash
#Inroduction:
#    用于检测各类tomcat是否正常。
#author: arno

TomcatFile='/arno/shell/tomcat_info.txt'
MAIL='Arno@ag866.com ai_yan125@126.com'

# 日志输出
GetPageInfo=/dev/null
TomcatMonitorLog=/tmp/TomcatMonitor.log
TomcatTempLog=/tmp/TomcatTemp.log

if [ ! -f "$TomcatFile" ];then
    RESULT="用于存储tomcat信息的/usr/local/shell/tomcat_info.txt文件不存在，请查看。"
    /usr/bin/printf $RESULT |/bin/mail -s "tomcat file alarm" $MAIL
    exit 0
fi

TOMCAT=$(cat $TomcatFile)

for TomcatInfo in $TOMCAT
do
    if [ -z $TomcatInfo ];then
    continue
    fi
    if [[ $TomcatInfo =~ ".*#.*" ]];then
    continue
    fi
    TomcatInfoUrl=$(echo $TomcatInfo |awk -F"|" '{print $1}')
    TomcatInfoInt=$(echo $TomcatInfo |awk -F"|" '{print $2}')
    TomcatHeadUrl=$(echo $TomcatInfo |awk -F"|" '{print $3}')
    if [ -z $TomcatHeadUrl ];then
        TomcatServiceCode=$(curl -s -o $GetPageInfo -m 10 --connect-timeout 10 $TomcatInfoUrl -w %{http_code})
    else
        TomcatServiceCode=$(curl -s -o $GetPageInfo -m 10 --connect-timeout 10 -H "Host:$TomcatHeadUrl" $TomcatInfoUrl -w %{http_code})
    fi
    CurrentTime=$(date +%Y/%m/%d-%H:%M:%S)
    if [ "$TomcatServiceCode" -eq 200 ];then
        echo "$CurrentTime $TomcatInfoInt:$TomcatHeadUrl $TomcatInfoUrl 检测正常。返回状态为：$TomcatServiceCode" >> $TomcatMonitorLog
    else
        RESULT="$CurrentTime $TomcatInfoInt:$TomcatHeadUrl $TomcatInfoUrl 检测失败。返回状态为：$TomcatServiceCode"
        echo $RESULT  >> $TomcatMonitorLog
        echo $RESULT  >> $TomcatTempLog
    fi
done
echo "----------------------------------------------" >> $TomcatMonitorLog
if [ -s $TomcatTempLog ];then
    echo "" >> $TomcatTempLog
    echo "注：该检测脚本在192.168.100.107:/usr/local/shell/上。" >> $TomcatTempLog
    /bin/mail -s "tomcat test alarm" $MAIL < $TomcatTempLog
    rm -rf $TomcatTempLog
fi
