__author__ = 'rigel'

import os
import ipaddress
from paramiko import SSHClient, SSHConfig, AutoAddPolicy, SSHException
#from /home/rigel/PycharmProjects/try1/sqlite/sql/chrome/content import finddata
import json
import time

def connect_remote(ssh, syst):
    #ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        #ssh.connect('192.168.56.101', username='rigel', password='password')
        global ipadd
        ipadd = syst['ipaddress']
        ssh.connect(syst['ipaddress'], username=syst['hostname'], password=syst['password'])
        ssh.exec_command("sudo updatedb;")
        #time.sleep(60)
        channel = ssh.invoke_shell()
        msg = channel.recv(1024)
        print(msg)
        stdin, stdout, stderr = ssh.exec_command("ls -l;cd Desktop;ls -l ")

        for line in stdout:
            print('...'+line.strip('\n'))

        '''ftp = ssh.open_sftp()
        #ftp.get('/home/rigel/remotefile','/home/rigel/vachoo')
        ftp.get('/home/rigel/test', '/home/rigel/testfindvach')
        ftp.close()
        ssh.close()'''
        channel.close()

    except SSHException:
        print("SSH failed")


def ftp_to_sys(ssh, pathInRem):
    ftp = ssh.open_sftp()
    path, name = pathInRem.rsplit('/', 1)
    #ftp.get('/home/rigel/remotefile','/home/rigel/vachoo')
    global ipadd
    pathInLocal = "/tmp/"+name+ipadd
    print("hello path: " + pathInLocal)
    ftp.get(pathInRem, pathInLocal)
    ftp.close()
    #ssh.close()   ##check if this is why back button was not working.....
    return pathInLocal


def searchpathfunc(ssh, InputParams):

    path = InputParams["dbpath"]
    print(path)
    stdin, stdout, stderr = ssh.exec_command("cd / ; locate " + path + '\n')

    listofpaths = dict()
    i = 0
    stdin.write('password\n')
    stdin.flush()
    for line in stdout:
        print('...'+line.strip('\n'))
        listofpaths[str(i)] = line.strip('\n')
        i = i+1

    return listofpaths


def copy_from_rem(ssh, pathInRem, pathInLocal):
    ftp = ssh.open_sftp()
    ftp.get(pathInRem, pathInLocal)
    ftp.close()


def commit_to_rem(ssh, inst_db_loc, ipadd, pathInRem, pathInLocal):
    ftp = ssh.open_sftp()
    path_dir = pathInRem.split('/')
    path_dir = path_dir[0:-1]
    path_dir = "/".join(path_dir)
    if ipadd in path_dir:
        ftp.put(pathInLocal, pathInRem)
    else:

        print("@@@@@@@@ path in remote -----> : " + pathInLocal + " path in instance " + inst_db_loc )
        ssh.exec_command("cd " + path_dir + "; mkdir " + ipadd )
       	time.sleep(5)
        ftp.put(pathInLocal, inst_db_loc)
    ftp.close()