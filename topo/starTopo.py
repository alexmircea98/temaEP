import time
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
import sys
from tests import *

def MyNetwork():

    net = Mininet( topo=None,
                   build=False,
                   link=TCLink,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    con1=net.addController(name='con1', controller=RemoteController)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')

    info( '*** Add hosts\n')
    
    client1 = net.addHost('client1', cls=Host, ip='10.0.0.10', defaultRoute=None, cpu=0.2)
   
    serv1 = net.addHost('serv1', cls=Host, ip='10.10.10.11', defaultRoute=None)
    serv2 = net.addHost('serv2', cls=Host, ip='10.10.10.12', defaultRoute=None)
    serv3 = net.addHost('serv3', cls=Host, ip='10.10.10.13', defaultRoute=None)
    
    info( '*** Add links\n')

    net.addLink(client1, s1, bw=1)

    net.addLink(s1, serv1, bw=10)
    net.addLink(s1, serv2, bw=4)
    net.addLink(s1, serv3, bw=4)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([con1])

    info( '*** Post configure switches and hosts\n')

    net.pingAll()
    net.iperf()

    info( '*** Run test if available\n')
    if len(sys.argv) >= 2:        
        if sys.argv[1] == "base":
            testbase(net)
    else:
        print("Unregonised test, starting cli")
        CLI(net)
    
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    MyNetwork()

