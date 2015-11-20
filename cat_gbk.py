#!/usr/bin/env python
#-_- coding: utf-8 -_-
'''
用于查看gbk格式的文件 --- 例如: fabric_info.txt
'''
import sys

with open(sys.argv[1], 'r') as file_open:
    for line in file_open.readlines():
        print line.decode('gbk'),



##以下用于将gbk格式的文件转换成utf-8的文件
#line_list = []
#with open(sys.argv[1], 'r') as file_open:
#    for line in file_open.readlines():
#        line_list.append(line.decode('gbk'),)
#
#with open('%s.bak' % sys.argv[1], 'a') as file_write:
#    for line in line_list:
#        file_write.write(line.encode('utf-8'))


