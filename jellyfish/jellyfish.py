#!/usr/bin/python 

"CS244 Spring 2013 Assignment 3: Jellyfish"

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser
from random import randrange

from monitor import monitor_qlen
import termcolor as T

import sys
import os
import math

parser = ArgumentParser(description="Jellyfish Tests")

parser.add_argument('-nse',
                    dest="nServers",
                    type=int,
                    action="store",
                    help="Number of servers",
                    default=16)

parser.add_argument('-nsw',
                    dest="nSwitches",
                    type=int,
                    action="store",
                    help="Number of switches",
                    default=20)

parser.add_argument('-np',
                     dest="nPorts",
                    type=int,
                    action="store",
                    help="Number of ports per switch",
                    default=4)

args = parser.parse_args()



class JFTopo(Topo):
    "Jellyfish Topology"

    def __init__(self, nServers, nSwitches, nPorts):
        super(JFTopo, self).__init()
        self.nServers = nServers
        self.nSwitches = nSwitches
        self.nPorts = nPorts
        self.create_topology()

    def create_topology(self):
        servers = []
        for n in range(self.nServers):
            servers.append(self.addHost('h%s' % n))
            #server["server" + n] 

        switches = []
        openPorts = []
        for n in range(self.nSwitches):
            switches.append(self.addSwitch('s%s' % n))
            openPorts.append(self.nPorts)
        
        # Connect each server with a switch
        for n in range(self.nServers):
            self.addLink(servers[n], switches[n]) #delay, bandwith?
            openPorts[n] -= 1
            # assume nPorts > 1
        
        # Manage the potential links, fully populate the set before creating
        links = set()
        switchesLeft = self.nSwitches
        consecFails = 0
        while switchesLeft > 1 and consecFails < 10:
            s1 = randrange(self.nSwitches)
            while openPorts[s1] == 0:
                s1 = randrange(self.nSwitches)

            s2 = randrange(self.nSwitches)
            while openPorts[s2] == 0 or s1 == s2:
                s2 = randrange(self.nSwitches)

            if (s1, s2) in links:
                consecFails += 1
            else:
                consecFails = 0
                links.add((s1, s2))
                links.add((s2, s1))

                openPorts[s1] -= 1
                openPorts[s2] -= 1

                if openPorts[s1] == 0:
                    switchesLeft -= 1

                if openPorts[s2] == 0:
                    switchesLeft -= 1

        if switchesLeft > 0:
            # post process
            pass

        for link in links:
            # prevent double counting
            if link[0] < link[1]:
                self.addLink(switches[link[0]], switches[link[1]])
        # while 
        # pick random switch (make sure has open port)
        # pick 2nd random diff switch
        # connect if not connected already, decrement count for each of the switches port count, if = 0, decrement total count
        # if not connect add to fail counter, when reached 10 break
        # if 0 finish
        # if 1, check # ports, if 2/3 call port expansion (connects empty ports to existing link that is not this node), if 4call twice
        

def jellyfish():
    topo = JFTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    dumpNodeConnections(net.hosts)
    net.pingAll()

    


    net.stop()
    # Ensure that all processes you create within Mininet are killed.       
    # Sometimes they require manual killing.                                
    Popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()

if __name__ == "__main__":
    jellyfish()
