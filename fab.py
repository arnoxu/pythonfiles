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

#local文件的内容的判断
def _contains(shell_name, big_cut):
    with settings(warn_only = True):
        big_cut_d = local('echo %s |sed \'s/ /, /g\'' % big_cut, capture = True)
        
        result = local('cat %s |egrep "%s"' % (shell_name, big_cut_d), capture = True)
    if result.failed:
        return False
    else:
        return True

def deploy():
    execute(_confirm)

#利用map()函数，把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。
#输入：['adam', 'LISA', 'barT']，输出：['Adam', 'Lisa', 'Bart']。
name_list = ['adam', 'LISA', 'barT']
def fn(name):
    return name.capitalize()
print map(fn, name_list)

#print map(lambda name: name.capitalize(), name_list)


#Python提供的sum()函数可以接受一个list并求和
#请编写一个prod()函数，可以接受一个list并利用reduce()求积。
num_list = [2, 3, 5, 6, 9]
def prod(num_list):
    def fn_product(x, y):
        return x * y
    return reduce(fn_product, num_list)
#print reduce(lambda x, y: x*y, [2, 3, 5, 6, 9])


#请尝试用filter()删除1~100的素数。
def not_primer(num):
    for i in range(2, int(num*0.5) + 1):
        if num % i == 0:
            return False
    else:
        return True
num_list2 = range(1, 101)




if __name__ == '__main__':
    print prod(num_list)
    print filter(not_primer, num_list2)

