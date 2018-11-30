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

#def message_contents():

def get_filename(message):
    """returns string file name retrieved from message"""
    message_deserialized = json.loads(message)
    filename = message_deserialized['filename'] #returns unicode
    return str(filename)

def file_exist(filename):
    """"return True if the given file exist in our directory"""
    if filename in listdir('./database'):
        return True
    return False

def handle_controller_connection(controller_socket):
    logger = open('log_ser_con.txt', 'a')
    request = controller_socket.recv(1024)
    logger.write('Controller: %s\n' % (request))
    message = message_files()
    controller_socket.send(message)
    logger.close()
    controller_socket.close()

def handle_controller(StoC_socket):
    while True:
        controller_sock, address = StoC_socket.accept()
        #print 'Accepted connection from {}:{}'.format(address[0], address[1])
        client_handler = threading.Thread(
            target=handle_controller_connection,
            args=(controller_sock,)
        )
        client_handler.start()

def handle_renderer_connection(renderer_socket):
    logger = open('log_ser_ren.txt', 'a')
    request = renderer_socket.recv(1024)
    logger.write('Renderer: %s\n' % (request))

    filename = get_filename(request)
    file_path = './database/' + filename
    f = open(file_path, 'rb')
    with open(file_path, 'rb') as f:
        l = f.read(1024)
        while(l):
            renderer_socket.send(l)
            l = f.read(1024)
    f.close()
    renderer_socket.send('Server: ACK received')
    logger.close()
    renderer_socket.close()

def handle_renderer(RtoS_socket):
    while True:
        renderer_sock, address = RtoS_socket.accept()
        #print 'Accepted connection from {}:{}'.format(address[0], address[1])
        client_handler = threading.Thread(
            target=handle_renderer_connection,
            args=(renderer_sock,)
        )
        client_handler.start()

def main():
    parser = optparse.OptionParser()
    parser.add_option('--is', dest='ips', default='10.0.0.1')
    parser.add_option('--ir', dest='ipr', default='10.0.0.3')
    (options, args) = parser.parse_args()
    bind_ip_ser = options.ips

    port_CtoS = 50000
    port_RtoS_command = 50002

    StoC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    StoC_socket.bind(("", port_CtoS))
    StoC_socket.listen(5)  # max backlog of connections

    RtoS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RtoS_socket.bind((bind_ip_ser, port_RtoS_command))
    RtoS_socket.listen(5)  # max backlog of connections

    pid = fork()

    if(pid == 0):
        handle_renderer(RtoS_socket)
    elif(pid > 0):
        handle_controller(StoC_socket)

if __name__ == '__main__':
    main()
