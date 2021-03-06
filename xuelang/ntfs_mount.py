#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re

ntfs_pattern = re.compile(r'File System Personality:  NTFS')
ntfs_device_node = re.compile(r'.*Device Node:.*')
device_dict = {}

def get_device_node():
    disk = subprocess.check_output(['ls', '-1', '/Volumes'])
    disk_list = disk.split("\n")
    for disk_name in disk_list[:-1]:
        disk_path = '/Volumes/' + disk_name
        try:
            disk_info = subprocess.check_output(['diskutil',
                                                 'info',
                                                 disk_path])
        except subprocess.CalledProcessError, e:
            print "diskutil stderr output:\n", e.output

        if ntfs_pattern.search(disk_info):
            device_node_str = ntfs_device_node.findall(disk_info)
            device_node = device_node_str[0].split()[2]
            device_dict[disk_path] = device_node


def mount_ntfs():
    if not device_dict:
        print "No ntfs filesystem found..."
        return
    print "hdiutil detach disk..."
    subprocess.check_output(['hdiutil', 'detach', device_dict.keys()[0]])
    for disk_path in device_dict.keys():
        device_node = device_dict[disk_path]
        print "mkdir %s" % disk_path
        subprocess.check_output(['mkdir', disk_path])
        print "sudo mount_ntfs -o rw,nobrowse %s %s" % (device_node, disk_path)
        subprocess.check_output(['sudo',
                                 'mount_ntfs',
                                 '-o',
                                 'rw,nobrowse',
                                 device_node, disk_path])


if __name__ == '__main__':
    get_device_node()
    mount_ntfs()
