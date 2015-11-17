#!/usr/bin/env python
#-_- coding: utf-8 -_-

#num = 100
#
#if num > 100:
#    print 'yes'
#elif num > 60:
#    print 'good'
#else:
#    print 'wrong'

big_cut = '  111:111 222:222  \t   \n '

except_list = ['', ' ', '\t', '\r', '\n']

big_cut_list = big_cut.split(' ')

print big_cut_list

for big_cut_e in big_cut_list:
    if big_cut_e in except_list:
        continue
    else:
        print "%s wrong" % big_cut_e





