"""
Description: Scan ipaddresses in your Home LAN. Get OS and currently up configuration
"""

__author__ = 'Sujayyendhiren Srinivasamurthi'
__email__ = 'sujayy1983@gmail.com'

import os
import nmap
import socket
import traceback
import subprocess
from netaddr import *

class LANNetworkInfo(object):
    """ Use nmap and get network data."""

    def __init__(self):
        """ Initialize object."""

        #Following parameters are candidate for config files
        self.networkRange = '192.168.0.0/28'
        self.devicesUp = []
        self.portRange = '22-80'
        self.output = None
        self.count = 0
        self.separator = '\n==========================\n'

    def GetHostListInNetwork(self):
        """ Get a list of IPs in a network. Copied this function from internet.""" 

        try:
            ipNet = IPNetwork(self.networkRange)
            hosts = list(ipNet)
            if len(hosts) > 2:
                hosts.remove(ipNet.broadcast)
                hosts.remove(ipNet.network)
            hostList = [str(host) for host in hosts]

            nm = nmap.PortScanner()
            
            for host in hostList:
                nm.scan(host, self.portRange) 
                hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

                for host, status in hosts_list:
                    self.devicesUp.append(host)
                    print('{0}:{1}'.format(host, status))
        except:
            exception = traceback.print_exc()
            print exception

    def logOutput(self, buffer, name=None):

        fileLog = None
        if name == None:
            #Check if file exists and create the one with new one.
            fileLog = open( './logs/' + str(name), 'w')
        else:
            fileLog = open( './logs/' + name, 'w')

        fileLog.write(buffer)
        fileLog.close()
    
    def identifyOS(self):
        try:
            print 'In progres ... ',
            for device in self.devicesUp:
                print '.',
                cmd = 'sudo nmap -PN -O ' + device 
                command = cmd.split(' ')
                process = subprocess.Popen( command, stdout=subprocess.PIPE)
                out, err = process.communicate()
                print '..',
                self.output = self.separator + "Output " + device + self.separator + str(out) + "\nError:\n" + str(err) + "\n"
                self.logOutput(self.output, 'Out'+device)
        except:
            exception = traceback.print_exc()
            print exception

if __name__ == '__main__':

    objLANInfo = LANNetworkInfo()
    objLANInfo.GetHostListInNetwork()
    objLANInfo.identifyOS()
