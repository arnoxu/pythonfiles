#!/usr/bin/env python
#-_- coding: utf-8 -_-
"""
write hosts in server.conf
"""
file_name = 'server.conf'
path = '/arno/shell'
hosts1 = '%s/hosts.txt' %path
hosts2 = '%s/wwwhosts.txt' %path
line_in = 'write hosts in server.conf\n'
file_list = []
hosts1_list = []
hosts2_list = []

f = open('%s/%s' % (path, file_name), 'r')
for i in f.readlines():
    file_list.append(i)
f.close

f = open(hosts1, 'r')
for i in f.readlines():
    hosts1_list.append(i)
f.close

f = open(hosts2, 'r')
for i in f.readlines():
    hosts2_list.append(i)
f.close

hosts1_list.reverse()
hosts2_list.reverse()

line_num = file_list.index(line_in)
#print file_list.index(line_in)
#print line_num
#print hosts1_list

for i in hosts1_list+hosts2_list:
    i = i.replace('\n', '')
#    print i
    if i == '':
        pass
    elif ('        <Alias>%s</Alias>\n' %i) in file_list:
        pass
    else:
        file_list.insert(line_num+1, '        <Alias>%s</Alias>\n' %i)
#print ''.join([i for i in file_list])

f = open('%s/%s' %(path, file_name), 'w')
for i in file_list:
    f.write(i)
f.close


