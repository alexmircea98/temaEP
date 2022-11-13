#!/usr/bin/python

"""
Adaptare dupa linuxrouter.py ( Example network with Linux IP router)
pentru Tema EP 2022

"""
# TODO: Adaugat comentarii si TODOs

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI
from contextlib import contextmanager
import sys, os
import hashlib
import argparse
from test import *

global band
band = []
global dela
dela = []
global los
los = []


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):

        
        # Adding 
        r0 = self.addNode( 'r0', cls=LinuxRouter, ip='10.10.200.1/24' )
        r1 = self.addNode( 'r1', cls=LinuxRouter, ip='10.10.101.1/24' )
        r2 = self.addNode( 'r2', cls=LinuxRouter, ip='10.10.102.1/24' )
        r3 = self.addNode( 'r3', cls=LinuxRouter, ip='10.10.103.1/24' )

        s0, s1, s2, s3 = [ self.addSwitch( s ) for s in ['s0', 's1', 's2', 's3'] ]

        self.addLink( s1, r1, intfName2='r1-eth1',
                      params2={ 'ip' : '10.10.101.1/24' }, 
                      bw=band[6], delay=dela[6], loss=los[6]
                      )  
        self.addLink( s2, r2, intfName2='r2-eth1',
                      params2={ 'ip' : '10.10.102.1/24' },
                      bw=band[7], delay=dela[7], loss=los[7]
                      )
        self.addLink( s3, r3, intfName2='r3-eth1',
                      params2={ 'ip' : '10.10.103.1/24' },
                      bw=band[8], delay=dela[8], loss=los[8])    

        
        self.addLink( s0, r0, intfName2='r0-eth1',
                      params2={ 'ip' : '10.10.200.1/24' }, 
                      bw=0.02, delay='0ms', loss=0
                      )  
        
        
        self.addLink(r1, r0,
                     intfName1='r1-eth2',intfName2='r0-eth2',
                     params1={'ip': '10.10.1.1/24'},
                     params2={'ip': '10.10.1.2/24'},
                     bw=band[9], delay=dela[9], loss=los[9]
                     )
        self.addLink(r2, r0,
                     intfName1='r2-eth2',intfName2='r0-eth3',
                     params1={'ip': '10.10.2.1/24'},
                     params2={'ip': '10.10.2.2/24'},
                     bw=band[10], delay=dela[10], loss=los[10]
                     )
        self.addLink(r3, r0,
                     intfName1='r3-eth2',intfName2='r0-eth4',
                     params1={'ip': '10.10.3.1/24'},
                     params2={'ip': '10.10.3.2/24'},
                     bw=band[11], delay=dela[11], loss=los[11]
                     )

        h1 = self.addHost( 'h1', ip='10.10.101.2/24',
                           defaultRoute='via 10.10.101.1' )
        h2 = self.addHost( 'h2', ip='10.10.101.3/24',
                           defaultRoute='via 10.10.101.1' )
        
        h3 = self.addHost( 'h3', ip='10.10.102.2/24',
                           defaultRoute='via 10.10.102.1' )
        h4 = self.addHost( 'h4', ip='10.10.102.3/24',
                           defaultRoute='via 10.10.102.1' )
        h5 = self.addHost( 'h5', ip='10.10.103.2/24',
                           defaultRoute='via 10.10.103.1' )
        h6 = self.addHost( 'h6', ip='10.10.103.3/24',
                           defaultRoute='via 10.10.103.1' )
        
        c1 = self.addHost( 'c1', ip='10.10.200.2/24',
                           defaultRoute='via 10.10.200.1' )
        

        
        self.addLink( c1, s0, bw=0.02, delay=0, loss=0 )
        self.addLink( h1, s1, bw=band[0], delay=dela[0], loss=los[0] ) 
        self.addLink( h2, s1, bw=band[1], delay=dela[1], loss=los[1] ) 
        self.addLink( h3, s2, bw=band[2], delay=dela[2], loss=los[2] ) 
        self.addLink( h4, s2, bw=band[3], delay=dela[3], loss=los[3] )
        self.addLink( h5, s3, bw=band[4], delay=dela[4], loss=los[4] ) 
        self.addLink( h6, s3, bw=band[5], delay=dela[5], loss=los[5] )
        

def routing(net):
    # Add routing for reaching networks that aren't directly connected
    info(net['r0'].cmd("ip route add 10.10.101.0/24 via 10.10.1.1 dev r0-eth2"))
    info(net['r0'].cmd("ip route add 10.10.102.0/24 via 10.10.2.1 dev r0-eth3"))
    info(net['r0'].cmd("ip route add 10.10.103.0/24 via 10.10.3.1 dev r0-eth4"))

    info(net['r1'].cmd("ip route add 10.10.200.0/24 via 10.10.1.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 10.10.102.0/24 via 10.10.1.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 10.10.103.0/24 via 10.10.1.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 10.10.2.0/24 via 10.10.1.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 10.10.3.0/24 via 10.10.1.2 dev r1-eth2"))

    info(net['r2'].cmd("ip route add 10.10.200.0/24 via 10.10.2.2 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.10.101.0/24 via 10.10.2.2 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.10.103.0/24 via 10.10.2.2 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.10.1.0/24 via 10.10.2.2 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.10.3.0/24 via 10.10.2.2 dev r2-eth2"))

    info(net['r3'].cmd("ip route add 10.10.200.0/24 via 10.10.3.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.10.101.0/24 via 10.10.3.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.10.102.0/24 via 10.10.3.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.10.1.0/24 via 10.10.3.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.10.2.0/24 via 10.10.3.2 dev r3-eth2"))

def gen_data(user):
    print(user)
    hash = hashlib.sha256(user.encode('utf-8')).hexdigest()
    print(hash)
    for i in range(12):
        band.append(float(int(hash[i:i+2], 16)%20+2)/1000)

    for i in range(12):
        dela.append('\''+str(int(hash[i+12:i+14], 16)%25)+'ms\'')

    for i in range(12):
        los.append(int(hash[i+24:i+26], 16)%3)

def run():
    "Test linux router"
    parser = argparse.ArgumentParser()
    parser.add_argument('user',
                        help='your moodle username')
    parser.add_argument('-t', '--test',
                        help='set it if you want to run tests',
                        action="store_true")
    cfg = parser.parse_args()

    gen_data(cfg.user)

    topo = NetworkTopo()
    net = Mininet( topo=topo, link=TCLink )  # 
    routing(net)
    net.start()
    info( '*** Routing Table on Router0:\n' )
    print(net[ 'r0' ].cmd( 'route' ))
    info( '*** Routing Table on Router1:\n' )
    print(net[ 'r1' ].cmd( 'route' ))
    info( '*** Routing Table on Router2:\n' )
    print(net[ 'r2' ].cmd( 'route' ))
    info( '*** Routing Table on Router3:\n' )
    print(net[ 'r3' ].cmd( 'route' ))
    
    # Testing area
    if cfg.test:        
        test(net)
    else:
        print("No test run, starting cli")
        
    CLI(net)
    
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
