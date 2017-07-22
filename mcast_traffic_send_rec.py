#! /usr/bin/env python
# send.mgn
# 0.0 ON 1 UDP DST 224.225.0.1/5000 PERIODIC [1000 64] INTERFACE eth2 
# 300.0 OFF 1

import sys
import paramiko
from socket import error as SocketError

class McastTraffic(object):

    def __init__(self):
        self.auth = False

    def connect(self, server, username=None, password=None):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if username and password:
                self.client.connect(server, username=username, password=password)
            self.auth = True
        except SocketError:
            self.auth = False
        except paramiko.AuthenticationException:
            self.auth = False

    def print_menu(self):
        print('What would you like to do: ')
        print('1. Send traffic')
        print('2. Capture traffic')
        print('3. Stop Capture')
        print('4. Get Results')
        print('5. Run command')
        print('6. Exit')

    def do_task(self, task, logfile):
        if not self.auth:
            return 'Error in connecting to %s'%host

        print "Executing task : %s"%(task)
        mgenfile = 'capture.drc' if task is 'capture' else 'send.mgen'
        stdin,stdout,stderr= self.client.exec_command("ssh root@169.254.0.3 /root/mcast-tools/src-mgen-5.02b/makefiles/mgen input {0} output {1}".format(mgenfile, logfile))
        print stdout.readlines()
    
    def kill_task(self):
        if not self.auth:
            return 'Error in connecting to %s'%host

        print "Executing kill operation"
        stdin,stdout,stderr= self.client.exec_command("ssh root@169.254.0.3 kill mgen")
        print stdout.readlines()
    
    def get_results(self, logfile):
        if not self.auth:
            return 'Error in connecting to %s'%host

        print "Executing get_results"
        stdin, stdout, stderr = self.client.exec_command("ssh root@169.254.0.3 grep \"RECV|SEND\" {} | wc -l".format(logfile))
        print stdin.readlines()
    
    def close_ssh(self):
        if not self.auth:
            return 'Error in connecting to %s'%host

        print "Executing close_ssh session"
        stdin, stdout, stderr = self.client.close()
	print stdout.readlines()
    
    def run_command(self, cmd):
        if not self.auth:
            return 'Error in connecting to %s'%host

        print "Executing run_command"
        stdin, stdout, stderr = self.client.exec_command(cmd)
	print stdout.readlines()

while True:
    mcast = McastTraffic()
    mcast.print_menu()
    choice = raw_input('Enter a number, hostname, logfile: ')
    choice_list = choice.split(",")
    choice = int(choice_list[0])
    hostip = choice_list[1] if choice_list[1] is not None else None
    logfile = choice_list[2] if choice_list[2] is not None else None

    #check if the above args are present before going to choices
    if choice == 1:
        mcast.connect(hostip, 'root', 'c0ntrail123')
        mcast.do_task('send', logfile)
    elif choice == 2:
        mcast.connect(hostip, 'root', 'c0ntrail123')
        mcast.do_task('capture', logfile)
    elif choice == 3:
        mcast.connect(hostip, 'root', 'c0ntrail123')
        mcast.kill_task()
    elif choice == 4:
        mcast.connect(hostip, 'root', 'c0ntrail123')
        mcast.get_results(logfile)
    elif choice == 5:
        mcast.connect(hostip, 'root', 'c0ntrail123')
        mcast.run_command(logfile)
    elif choice == 6:
        print "quitting"
        break
