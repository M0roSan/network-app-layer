#!/usr/bin/python
import socket, optparse
import threading
from os import listdir, fork

import json

def message_files():
    """Create message: JSON like object"""
    contents = [file for file in listdir('./database')]
    message = {'filename': None, 'request': None, 'contents': contents}
    message_serialized = json.dumps(message)
    return message_serialized

def handle_controller_connection(controller_socket):
    logger = open('log_ser.txt', 'a')
    request = controller_socket.recv(1024)
    logger.write('Received %s\n' % (request))
    message = message_files()
    controller_socket.send(message)
    logger.close()
    controller_socket.close()

def handle_controller(StoC_socket):
    while True:
        controller_sock, address = StoC_socket.accept()
        print 'Accepted connection from {}:{}'.format(address[0], address[1])
        client_handler = threading.Thread(
            target=handle_controller_connection,
            args=(controller_sock,)
        )
        client_handler.start()

def main():
    parser = optparse.OptionParser()
    parser.add_option('--ir', dest='ipr', default='')
    parser.add_option('--is', dest='ips', default='')
    (options, args) = parser.parse_args()
    bind_ip = options.ips
    port_CtoS = 50000
    StoC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    StoC_socket.bind((bind_ip, port_CtoS))
    StoC_socket.listen(5)  # max backlog of connections

    pid = fork()

    if pid == 0:
        #do something
    elif pid > 0:
        handle_controller(StoC_socket)

if __name__ == '__main__':
    main()