#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call


def myNetwork():
    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8')

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='127.0.0.1',
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s21 = net.addSwitch('s21', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s22 = net.addSwitch('s22', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s18 = net.addSwitch('s18', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s19 = net.addSwitch('s19', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s20 = net.addSwitch('s20', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s17 = net.addSwitch('s17', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s16 = net.addSwitch('s16', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s15 = net.addSwitch('s15', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s23 = net.addSwitch('s23', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s24 = net.addSwitch('s24', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s25 = net.addSwitch('s25', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s26 = net.addSwitch('s26', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s27 = net.addSwitch('s27', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s28 = net.addSwitch('s28', cls=OVSKernelSwitch, protocols='OpenFlow13')
    s29 = net.addSwitch('s29', cls=OVSKernelSwitch, protocols='OpenFlow13')


    info('*** Add links\n')
    net.addLink(s1, s2)
    net.addLink(s3, s2)
    net.addLink(s3, s6)
    net.addLink(s4, s3)
    net.addLink(s4, s7)
    net.addLink(s5, s4)
    net.addLink(s6, s7)
    net.addLink(s6, s8)
    net.addLink(s8, s5)
    net.addLink(s9, s8)
    net.addLink(s10, s6)
    net.addLink(s10, s26)
    net.addLink(s11, s1)
    net.addLink(s11, s3)
    net.addLink(s21, s9)
    net.addLink(s21, s22)
    net.addLink(s18, s7)
    net.addLink(s19, s7)
    net.addLink(s20, s7)
    net.addLink(s12, s11)
    net.addLink(s13, s12)
    net.addLink(s16, s13)
    net.addLink(s16, s17)
    net.addLink(s14, s13)
    net.addLink(s15, s14)
    net.addLink(s23, s24)
    net.addLink(s24, s25)
    net.addLink(s25, s10)
    net.addLink(s26, s27)
    net.addLink(s27, s28)
    net.addLink(s28, s29)
    net.addLink(s29, s23)

    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    net.addLink(h1, s1)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    net.addLink(h3, s27)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    net.addLink(h2, s1)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s7').start([c0])
    net.get('s6').start([c0])
    net.get('s8').start([c0])
    net.get('s9').start([c0])
    net.get('s10').start([c0])
    net.get('s11').start([c0])
    net.get('s21').start([c0])
    net.get('s22').start([c0])
    net.get('s18').start([c0])
    net.get('s19').start([c0])
    net.get('s20').start([c0])
    net.get('s17').start([c0])
    net.get('s12').start([c0])
    net.get('s13').start([c0])
    net.get('s16').start([c0])
    net.get('s14').start([c0])
    net.get('s15').start([c0])
    net.get('s23').start([c0])
    net.get('s24').start([c0])
    net.get('s25').start([c0])
    net.get('s26').start([c0])
    net.get('s27').start([c0])
    net.get('s28').start([c0])
    net.get('s29').start([c0])



if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()

topos = {'mytopo': (lambda: myNetwork())}
