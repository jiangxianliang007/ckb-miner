#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 13:51
# @Author  : 007
# @File    : run_ckb_miner.py
# @Software: PyCharm

"""
An operation and maintenance tool for quickly running ckb miner nodes in batches.
"""

import paramiko
import threading
import os
import requests
import time


def downloader(url, path):
    """
    Download the CKB binary package
    """
    start = time.time()
    size = 0
    response = requests.get(url, stream=True)
    chunk_size = 1024
    content_size = int(response.headers['content-length'])
    if response.status_code == 200:
        print('[File size]: %0.2f MB' % (content_size / chunk_size / 1024))
        with open(path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size += len(data)
                print('\r' + '[Download progress]: %s %.2f%%' %
                      ('>' * int(size * 100 / content_size),
                       float(size / content_size * 100)),
                      end='')
    end = time.time()
    print('\n' + "[All download completed!]: %.2f second" % (end - start))


def put_ckb_binary(ip, username, passwd, ckb_binary_tar, remotedir):
    """
    Upload ckb binary to the mining server
    """
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=username, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        print("Uploading CKB binary to node %s ........." % ip)
        sftp.put(ckb_binary_tar, remotedir)
        t.close()
    except Exception as e:
        print("Server %s %s ,please check if the user password is correct." %
              (ip, e))


def connect_ckb_server(ip, username, passwd, cmd):
    """
    Connect to the server to execute the specified command
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=5)
        for m in cmd:
            print(m)
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            for o in out:
                print(o),
        print('%s\t connection succeeded .\n' % (ip))
        ssh.close()
    except:
        print(
            'Server %s connection failed, please check if the user password is correct.\n'
            % (ip))


def run_ckb_miner(ckb_version, ckb_binary_tar):
    """
    Mining entrance function
    """

    if os.path.exists(ckb_binary_tar):
        print('{} exists'.format(ckb_binary_tar))
        execut()
    else:
        print('{} does not exist'.format(ckb_binary_tar))
        dir = os.getcwd()
        path = dir + '/' + ckb_binary_tar
        url = "https://github.com/nervosnetwork/ckb/releases/download/%s/%s" % (ckb_version, ckb_binary_tar)
        print (url)
        print (path)
        downloader(url, path)
        execut()

def killall_miner():
    print("killall ckb miner ......")
    killall_miner_threads = []
    for ip in iplist:
        cmd = ([
            ('killall ckb')
        ])
        connect_thread = threading.Thread(target=connect_ckb_server,
                                            args=(ip, username, passwd, cmd))
        killall_miner_threads.append(connect_thread)

    for t in killall_miner_threads:
        t.setDaemon(True)
        t.start()

    for t in killall_miner_threads:
        t.join()


def execut():
    """
    run ckb miner
    """
    threads = []
    for ip in iplist:
        put_thread = threading.Thread(target=put_ckb_binary,
                                      args=(ip, username, passwd, ckb_binary_tar,
                                            remotepath))
        put_thread.start()
        put_thread.join()
    
    ckb_miner_threads = []
    for ip in iplist:
        cmd = ([(
            'cd %s;killall ckb;rm -rf ckb_%s_x86_64-unknown-linux-gnu;'
            'tar zxf ckb_%s_x86_64-unknown-linux-gnu.tar.gz;cd ckb_%s_x86_64-unknown-linux-gnu;'
            './ckb init -C ckb-testnet --chain testnet;'
            'sed -i "s/127.0.0.1/%s/" ./ckb-testnet/ckb-miner.toml;'
            'sed -i "s/threads     = 1/threads     = %d/" ./ckb-testnet/ckb-miner.toml;'
            'cd ckb-testnet;nohup ../ckb miner &' %
            (remotedir, ckb_version, ckb_version, ckb_version, ckb_node_ip, miner_threads))])
        connect_thread = threading.Thread(target=connect_ckb_server,
                                          args=(ip, username, passwd, cmd))
        ckb_miner_threads.append(connect_thread)

    for t in ckb_miner_threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    time.sleep(3)


if __name__ == '__main__':
    """
    The default variable configuration can be customized, such as: username, passwd, remotedir, iplist
    """
    username = "root"
    passwd = "pIve7NSHPjfjCZ8"
    remotedir = '/usr/local/src'
    ckb_version = "v0.15.6"
    miner_threads = 3 
    ckb_binary_tar = 'ckb_%s_x86_64-unknown-linux-gnu.tar.gz' % (ckb_version)
    remotepath = ("%s/%s" % (remotedir, ckb_binary_tar))
    ckb_node_ip = "192.168.1.100"
    iplist = ['192.168.1.101', '192.168.1.102']
    exit_flag = False
    menu = {
        1: 'run_ckb_miner',
        2: 'kill_ckb_miner',
        3: 'quit'
    }

    while not exit_flag:
        print("\n")
        for index, item in menu.items():
            print(index, item)
        choice = input("Choose to enter>>:")
        if choice.isdigit():
            choice = int(choice)
            if choice in list(menu.keys()):
                if choice == 1:
                    run_ckb_miner(ckb_version, ckb_binary_tar)
                elif choice == 2:
                    killall_miner()
                elif choice == 3:
                    exit_flag = True
            else:
                print(
                    "The entered code %d does not exist, please re-select !" %
                    choice)
        else:
            print(
                "=======Invalid option, please enter the number in the menu bar list======"
            )
