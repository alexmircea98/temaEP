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

        s0, s1, s2 = [ self.addSwitch( s ) for s in ['s0', 's1', 's2'] ]

        self.addLink( s1, r1, intfName2='r1-eth1',
                      params2={ 'ip' : '10.10.101.1/24' } 
                      #bw=100, delay='10ms', loss=0
                      )  
        self.addLink( s2, r2, intfName2='r2-eth1',
                      params2={ 'ip' : '10.10.102.1/24' } 
                      #bw=100, delay='10ms', loss=0
                      )  

        
        self.addLink( s0, r0, intfName2='r0-eth1',
                      params2={ 'ip' : '10.10.200.1/24' } 
                    # bw=100, delay='10ms', loss=0
                      )  
        
        
        self.addLink(r1, r0,
                     intfName1='r1-eth2',intfName2='r0-eth2',
                     params1={'ip': '10.10.1.1/24'},
                     params2={'ip': '10.10.1.2/24'},
                    # bw=100, delay='10ms', loss=0
                     )
        self.addLink(r2, r0,
                     intfName1='r2-eth2',intfName2='r0-eth3',
                     params1={'ip': '10.10.2.1/24'},
                     params2={'ip': '10.10.2.2/24'}
                    #bw=100, delay='10ms', loss=0
                     )


        h1 = self.addHost( 'h1', ip='10.10.101.2/24',
                           defaultRoute='via 10.10.101.1' )
        h2 = self.addHost( 'h2', ip='10.10.101.3/24',
                           defaultRoute='via 10.10.101.1' )
        
        h3 = self.addHost( 'h3', ip='10.10.102.2/24',
                           defaultRoute='via 10.10.102.1' )
        h4 = self.addHost( 'h4', ip='10.10.102.3/24',
                           defaultRoute='via 10.10.102.1' )
        
        c1 = self.addHost( 'c1', ip='10.10.200.2/24',
                           defaultRoute='via 10.10.200.1' )
        


        for h, s in [ (c1, s0),
                      (h1, s1), (h2, s1), 
                      (h3, s2), (h4, s2) 
        ]:                    # 100 Mbps, 10ms delay, no packet loss
            self.addLink( h, s, bw=100, delay='10ms', loss=0)

def routing(net):
    # Add routing for reaching networks that aren't directly connected
    info(net['r0'].cmd("ip route add 10.10.101.0/24 via 10.10.1.1 dev r0-eth2"))
    info(net['r0'].cmd("ip route add 10.10.102.0/24 via 10.10.2.1 dev r0-eth3"))

    info(net['r1'].cmd("ip route add 10.10.200.0/24 via 10.10.1.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 10.10.102.0/24 via 10.10.1.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 10.10.2.0/24 via 10.10.1.2 dev r1-eth2"))

    info(net['r2'].cmd("ip route add 10.10.200.0/24 via 10.10.2.2 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.10.101.0/24 via 10.10.2.2 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.10.1.0/24 via 10.10.2.2 dev r2-eth2"))

def run():
    "Test linux router"
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
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
