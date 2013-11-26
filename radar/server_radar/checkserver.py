'''
Created on Jul 26, 2011

@author: oquidave
'''
import os
import subprocess
import re
import socket
import paramiko
from datetime import *
from radar.sysradar_tools.EmailSms import EmailSms

class Radar():
    '''
    a couple of modules that monitor the infrastructure
    '''

    def __init__(self, hostname=''):
        '''
        Constructor
        '''
        self.hostname = hostname
        
   
    def get_time_obj(self, time_str):
        h, m, s = map(int, str(time_str).split(':'))
        time_obj = time(h, m, s)
        return time_obj
    
    def alert_time(self):
        """this method ensures that i don't get alerts at midnight, Admins also sleep!!!!!!!!"""
        weekend_alert_times = {'sat':{'start_time':'09:00:00', 'end_time':'17:00:00'},
                            'sun':{'start_time':'09:00:00', 'end_time':'15:00:00'}}    
        # get current time object
        now = datetime.time(datetime.now())
        week_day = int(datetime.now().strftime('%w'))
        if week_day >= 1 and week_day <= 5:
            "these are week days"
            start_time = "08:00:00";end_time = "17:00:00"
            start_time = self.get_time_obj(start_time);end_time = self.get_time_obj(end_time)
            # now = datetime.time(now)
            if now >= start_time and now <= end_time:
                return True
            else:
                return False
        else:
            if week_day == 6:
                day = 'sat'
            elif week_day == 7:
                day = 'sun'
            start_time = weekend_alert_times['%s' % (day)]['start_time'];end_time = weekend_alert_times['%s' % (day)]['end_time']
            start_time = self.get_time_obj(start_time);end_time = self.get_time_obj(end_time)
            # now = datetime.time(now)
            if now >= start_time and now <= end_time:
                return True
            else:
                return False
        
    
    def remote_cmd(self, box, hostname, username, password, cmd):
        """execute a command in a remote box using ssh """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
        ssh.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
    def box_alive(self, hostname=''):
        """check if a a certain box is up and running"""
        if hostname is None:
            hostname = self.hostname
        "check the ip add of a certainn server"
        cmd = "ping -c 3 %s" % (hostname)
        print(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        "get the cli output"
        # pattern_alive = '64 bytes from %s: icmp_req=' % hostname
        pattern_alive = r"^64 bytes from %s" % hostname
        pattern_dest_unreachable = r"Destination Host Unreachable"
        # pattern = 'plugtmp'
        line_counter = 1
        for cli_line in p.stdout.readlines():
            if line_counter == 1:
                line_counter += 1
                continue
            print(cli_line)
            # for res in re.finditer(pattern_alive, cli_line)
            match = re.compile(pattern_alive).search(cli_line)
            print("pattern_alive: " + pattern_alive + "\ncli_line: " + pattern_alive)
            if match:
                "server is alive"
                # print("server is alive")
                return True
            else:
                "server is not alive"
                # print("server is NOT alive")
                return False
            line_counter += 1
        
    def sendmsg(self, msg):
        "send concerned email and sms messages"
        # first check for time
        if self.alert_time():
            emailsms = EmailSms()
            print msg
            email_msg = sms_msg = msg
            # send sms
            emailsms.sms_blaster(sms_msg)
            # send email
            emailsms.email_blaster(email_msg)
        
    
    def port_check(self, address, port):
        # create a TCP socket
        s = socket.socket()
        print "Attempting to connect to %s on port %s" % (address, port)
        try:
            s.connect((address, port))
            print "Connected to to %s on port %s" % (address, port)
            return True
        except socket.error, e:
            print "Connection to to %s on port %s failed \n Error: %s" % (address, port, e)
            return False
    
    
    def service_check(self, address, port):
        "lets first start by checking if the monitor is even connected to the network"
        # connect: Network is unreachable
        # lets first check if the box is up
        service_status = ""
        if self.box_alive(address):
            """box is up so let's go ahead and check if certain service is working"""
            if self.port_check(address, port):
                service_status = "service_up"
            else: 
                service_status = "service_down"
        else:
            service_status = "box_down"
        print(service_status)
        return service_status
        
    def service_control(self, daemon, action, password):
        cmd = "sudo -S /etc/init.d/" + daemon + " " + action
        print "cmd: " + cmd
        if os.popen(cmd, "w").write(password):
            return True
        else:
            return False
        
        
        
        
        
            
          
