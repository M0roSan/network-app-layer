#!/usr/bin/python
import socket, optparse
import threading
import os, fcntl
from os import listdir, fork
from message import Message
import time, errno

q = ['first item']
qLock = threading.Lock()

def handle_controller_connection(controller_socket):
    request = controller_socket.recv(1024)
    print('Controller: {}\n'.format(request))
    contents = [file for file in listdir('./database')]
    message = Message(payload=contents)
    controller_socket.send(message.export())
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

def handle_renderer_connection(renderer_socket):
    while True:

        try:
            request = renderer_socket.recv(1024)
            print('Renderer: {}\n'.format(request))
        except socket.error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                sleep(1)
                print 'No data available'
                continue
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        message_rec = Message()
        message_rec.decode(request)
        filename = message_rec.filename

        if message_rec.command == 2: #PLAY
            filename = message_rec.filename
            file_path = './database/' + str(filename)
            message_send = Message()
            
            try:
                with open(file_path, 'rb') as f:
                    contents = f.read(1024)
                    while(contents):
                        print('reading another 1024')
                        qLock.acquire()
                        item = q.pop()
                        qLock.release()
                        if item == 'stop':
                            break

                        message_send.payload = contents
                        renderer_socket.send(message_send.export())
                        contents = f.read(1024)
                        qLock.acquire()
                        q.append('dummy')
                        qLock.release()
                        time.sleep(1)
                f.close()
            except:
                message_send.payload('File does not exist')
                renderer_socket.send(message_send.export())
        if message_rec.command == 3: #STOP
            qLock.acquire()
            q.append('stop')
            qLock.release()
            print('stop playing')
        if message_rec.command == 4: #RESUME
            qLock.acquire()
            q.append('resume')
            qLock.release()
            print('resume playing')

        renderer_socket.close()

def handle_renderer(RtoS_socket):
    while True:
        renderer_sock, address = RtoS_socket.accept()
        print 'Accepted connection from {}:{}'.format(address[0], address[1])
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
    RtoS_socket.bind(("", port_RtoS_command))
    fcntl.fcntl(RtoS_socket, fcntl.F_SETFL, os.O_NONBLOCK)
    RtoS_socket.listen(5)  # max backlog of connections

    pid = fork()

    if(pid == 0):
        handle_renderer(RtoS_socket)
    elif(pid > 0):
        handle_controller(StoC_socket)

if __name__ == '__main__':
    main()
