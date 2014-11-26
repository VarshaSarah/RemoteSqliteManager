__author__ = 'rigel'
import os
#os.system('echo "hello world"')
#os.system(' ls -l')
import ipaddress
import paramiko
import sys
#import cmd
ip = ipaddress.ip_address('192.168.56.102')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('192.168.56.102', username='rigel', password='password')
    channel = ssh.invoke_shell()
    msg = channel.recv(1024)
    print(msg)
    stdin, stdout, stderr = ssh.exec_command("ls -l;cd Desktop;ls -l ")
   # stdin, stdout, stderr = ssh.exec_command("cd Desktop")
   # stdin, stdout, stderr = ssh.exec_command("ls -l")
   # stdin.write('password\n')
   # stdin.flush()
    for line in stdout:
        print('...'+line.strip('\n'))
    ssh.close()
    channel.close()

except paramiko.SSHException:
    print("SSH failed")
#paramiko.ssh_exception.AuthenticationException




#type(stdin);
#stdout.readlines();

#/*
#channel = ssh.invoke_shell()
#msg = channel.recv(1024)
#print(msg)
#channel.send("ls")
#msg = channel.recv(1024)
#print(msg)
#*/


#sys.stdin = channel.makefile('wb')
#stdout = channel.makefile('rb')
#stdin.write("ls")
#print(stdout.read())
#stdin.close()
#stdout.close()
#for f in (sys.stderr, sys.stdin, sys.stdout) : print(f) no error
#print(sys.stdout.readlines())                            no error
#    = ssh.exec_command("ls -l")
#sys.stdin, sys.stderr = ssh.exec_command("ls -l")
#sys.stdout, stdin, stderr =
#print(stdout.readlines())
ssh.close()



#os.system("ls -l")
#os.system('ssh rigel@192.168.56.102')


#username = raw_input("Enter IP address ")
#ip = ipaddress("username");
#print( "hello, ", username)
#hostname = input("Enter hostname ")
#print("hostname",hostname)
#os.system('ssh '+hostname+'@'+username)
#print('ssh '+hostname+'@'+username)