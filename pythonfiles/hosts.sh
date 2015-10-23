#!/bin/bash
path='/arno/shell'
file=server.conf
hosts1='/arno/shell/hosts.txt'
hosts2='/arno/shell/wwwhosts.txt'

for i in $(cat $hosts1)
do 
#    echo $i
    sed -i '1 a\         <Alias>'"$i"'</Alias>' $path/$file
done

for i in $(cat $hosts2)
do
    sed -i '1 a\         <Alias>'"$i"'</Alias>' $path/$file
done
