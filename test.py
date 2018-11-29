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

    h1.setIP('10.0.0.1')
    h2.setIP('10.0.0.2')
    h3.setIP('10.0.0.3')

    #p1 = h1.popen('python server.py &') # server opens up and works in background

    #p3 = h3.popen('python renderer.py &') # renderer opens up and works in background

    ### WARNING ###
    # order matters. Don't switch p1 and p3


    CLI( net )
    p1.terminate()
    p3.terminate()
    net.stop()
    #------------------------------------------------------------------------#

if __name__ == '__main__':
    main()
