'''
Created on Jul 26, 2011

@author: oquidave
'''
import subprocess
import re
import socket
import paramiko
from datetime import *
from sysradar_tools.EmailSms import EmailSms

class Box():
    '''
    a couple of modules that monitor the infrastructure
    '''

    def __init__(self, hostname=''):
        '''
        Constructor
        '''
        self.hostname = hostname
        
    def boxes(self):
        "server ports of each server"
        boxes = {}
        boxes['mtn'] = {'ip':'192.168.2.99',
                        'logins':{'username':'dokwii', 'passwd': 's0z0n0w'},
               'server_ports':{'apache': '80', 'postgres':'5432', 'kannel':'13002'}
               }
        boxes['warid'] = {'ip':'192.168.2.171',
                          'logins':{'username':'dokwii', 'passwd': 's0z0n0w'},
               'server_ports':{'apache': '80', 'postgres':'5432', 'kannel':'13002'}
               }
        boxes['utl'] = {'ip':'192.168.2.174',
                        'logins':{'username':'dokwii', 'passwd': 's0z0n0w'},
               'server_ports':{'apache': '80', 'postgres':'5432', 'kannel':'13003'}
               }
        boxes['orange'] = {'ip':'192.168.2.178',
                           'logins':{'username':'dokwii', 'passwd': 's0z0n0w'},
               'server_ports':{'apache': '80', 'postgres':'5432', 'kannel':'13002'}
               }
        boxes['airtel'] = {'ip':'41.190.128.26',
                           'logins':{'username':'dokwii', 'passwd': 's0z0n0w'},
               'server_ports':{'apache': '80', 'postgres':'5432', 'kannel':'13001'}
               }
        '''boxes['devp_211'] = {'ip':'192.168.2.211',
               'server_ports':{'apache': '80', 'postgres':'5432', 'kannel':'13001'}
               }'''
        return boxes
    
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
        
    def box_alive(self, hostname=''):
        if hostname is None:
            hostname = self.hostname
        "check the ip add of a certainn server"
        cmd = "ping -c 3 %s" % (hostname)
        # cmd = "ls /tmp"
        # stdin, stdout, stderr = subprocess.call(cmd, shell=True)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        "get the cli output"
        # print p.stdout.read()
        # cli_output = stdout.readline
        # 64 bytes from 192.168.2.1: icmp_req=3 ttl=64 time=0.498 ms
        pattern_alive = '64 bytes from %s: icmp_req=' % hostname
        pattern_dest_unreachable = "Destination Host Unreachable"
        # pattern = 'plugtmp'
        line_counter = 1
        for cli_line in p.stdout.readlines():
            if line_counter == 1:
                line_counter += 1
                continue
            re_obj = re.compile(pattern_alive)
            match = re_obj.search(cli_line)
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
    
    def smsc_status(self, re_obj_online, re_obj_offline, cli_line, smsc, box, hostname):
        match_online = re_obj_online.search(cli_line)
        if match_online:
            "this smsc is online"
            print "smsc %s on box %s ip %s is online" % (smsc, box, hostname)
        else:
            "this smsc should be offline"
            match_offline = re_obj_offline.search(cli_line)
            if match_offline:
                msg = "smsc %s on box %s ip %s is offline" % (smsc, box, hostname)
                self.sendmsg(msg)
            else:
                "smsc is dead"
                msg = "smsc %s on box %s ip %s is dead" % (smsc, box, hostname)
                self.sendmsg(msg)
    
    def smsc_check(self, box, hostname, username, password, cmd):
        """check if the network smsc are on or not  """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
        ssh.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # if stderr.read() is None:
        "the cli output, check if smsc is alive or not"
        # smsc1    SMPP:193.108.253.202:3723/3723:smsads: (online 201935s,
        # smsc6    SMPP:41.223.85.7:9003/9003:faf:CMT (re-connecting, rcvd 0,

        smsc1_pattern = 'smsc1'
        smsc2_pattern = 'smsc2'
        smsc3_pattern = 'smsc3'
        smsc6_pattern = 'smsc6'
        online_pattern = 'online'
        offline_pattern = 're-connecting'
        re_obj_1 = None
        re_obj_2 = None
        re_obj_3 = None
        if box == 'mtn':
            re_obj_1 = re.compile(smsc1_pattern)
            re_obj_2 = re.compile(smsc2_pattern)
        elif box == 'utl':
            re_obj_1 = re.compile(smsc1_pattern)
            re_obj_3 = re.compile(smsc3_pattern)
        elif box == 'airtel':
            re_obj_1 = re.compile(smsc6_pattern)
            re_obj_3 = re.compile(smsc3_pattern)
        elif box == 'warid':
            re_obj_2 = re.compile(smsc2_pattern)
        elif box == 'orange':
            re_obj_1 = re.compile(smsc1_pattern)
            
        re_obj_online = re.compile(online_pattern)
        re_obj_offline = re.compile(offline_pattern)

        for cli_line in stdout.readlines():
            "check for line with smsc connection status"
            if re_obj_1:
                match_1 = re_obj_1.search(cli_line)
                if match_1:
                    # get this smsc
                    smsc = re_obj_1.findall(cli_line)[0]
                    "now check if online or not"
                    self.smsc_status(re_obj_online, re_obj_offline, cli_line, smsc, box, hostname)
            if re_obj_2:
                match_2 = re_obj_2.search(cli_line)
                if match_2:
                    smsc = re_obj_2.findall(cli_line)[0]
                    "now check if online or not"
                    self.smsc_status(re_obj_online, re_obj_offline, cli_line, smsc, box, hostname)
            if re_obj_3:
                match_3 = re_obj_3.search(cli_line)
                if match_3:
                    smsc = re_obj_3.findall(cli_line)[0]
                    "now check if online or not"
                    self.smsc_status(re_obj_online, re_obj_offline, cli_line, smsc, box, hostname)
 
    def server_check(self):
        "check the port a certain server"
        boxes = self.boxes()
        for box, box_details in boxes.iteritems():
            box_ip = box_details['ip']
            logins = box_details['logins']
            server_ports = box_details['server_ports']
            "first check if this box is alive"
            status = self.box_alive(box_ip)
            if status:
                # box is alive, now check for servers
                print "Box %s is alive, now checking for servers on this box" % (box)
                for k, v in server_ports.iteritems():
                    server_port = v
                    if k == 'apache':
                        server_name = 'apache'
                    elif k == 'postgres':
                        server_name = 'postgres'
                    elif k == 'kannel':
                        server_name = 'kannel'
                    port_status = self.port_check(box_ip, int(v))
                    if port_status:
                        print "%s server is ALIVE on box %s on ip %s port %s" % (server_name, box, box_ip, server_port)
                        # 'and (box == 'mtn' or box == 'utl' or box == 'airtel'), or 'and box in ('mtn', 'utl', 'airtel')'
                        if server_name == 'kannel' and box in ('mtn', 'utl', 'airtel', 'warid', 'orange'):
                            "check if the network smsc are on or not"
                            # lynx -dump 'http://localhost:13002/status?password=bar'
                            cmd = "lynx -dump 'http://localhost:%s/status?password=bar'" % (server_port)
                            hostname = box_ip; username = logins['username']; password = logins['passwd']
                            self.smsc_check(box, hostname, username, password, cmd)
                            
                        # return True
                    else:
                        msg = "%s server is DOWN on box %s, ip %s, port %s" % (server_name, box, box_ip, v)
                        "send concerned email and sms messages.Pliz check"
                        self.sendmsg(msg)      
                        
            else:
                msg = "Box %s is DOWN" % (box)
                self.sendmsg(msg)
                
