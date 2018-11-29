#!/usr/bin/python
from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI

def main():
    lg.setLogLevel('info')

    net = Mininet(SingleSwitchTopo(k=3))
    net.start()

    h1 = net.get('h1') #server
    h2 = net.get('h2') #controller
    h3 = net.get('h3') #renderer

    p1 = h1.popen('python server.py --is %s --ir %s&' % (h1.IP(), h3.IP()))

    #p3 = h3.popen('python renderer.py --ir %s --is %s &' % (h3.IP(), h1.IP()))

    #below here can be done in CLI.
    #-----------------------------------------------------------------------#
    h2.cmd('python controller.py --is %s --ir %s -c 1' % (h1.IP(), h3.IP())) #REQUST message

    

    #h2.cmd('python controller.py --is %s --ir %s -c 2' % (h1.IP(), h3.IP())) #PLAY message
    #h2.cmd('python controller.py --is %s --ir %s -c 3' % (h1.IP(), h3.IP())) #STOP message
    #h2.cmd('python controller.py --is %s --ir %s -c 4' % (h1.IP(), h3.IP())) #RESUME message
    #h2.cmd('python controller.py --is %s --ir %s -c 5' % (h1.IP(), h3.IP())) #PLAY_FROM_BEGINNING message


    CLI( net )
    p1.terminate()
    #p3.terminate()
    net.stop()
    #------------------------------------------------------------------------#

if __name__ == '__main__':
    main()
