import socket, optparse
import threading
from os import fork

def handle_command_connection(controller_socket, RtoS_socket):
    logger = open('log_ren_comm.txt', 'a')
    request = controller_socket.recv(1024)
    logger.write('Controller: %s\n' % (request))
    controller_socket.send('ACK-renderer')
    RtoS_socket.send(request)
    response = RtoS_socket.recv(4096)
    logger.write('Server: %s\n' % (response))
    logger.flush()
    logger.close()
    controller_socket.close()

def handle_command(RtoC_socket, RtoS_socket):
    while True:
        controller_sock, address = RtoC_socket.accept()
        #print 'Accepted connection from {}:{}'.format(address[0], address[1])
        client_handler = threading.Thread(
            target=handle_command_connection,
            args=(controller_sock,RtoS_socket,)
        )
        client_handler.start()
        
def handle_contents(RtoS_socket):
    while True:
        server_sock, address = RtoS_socket.accept()
        logger = open('log_ren_cont.txt', 'a')
        contents = server_sock.recv(1024)
        RtoS_socket.send('Renderer cont: acked\n')
        logger.write('Server contents: %s\n' %(contents))
        logger.flush()
    logger.close()


def main():
    parser = optparse.OptionParser()
    parser.add_option('--is', dest='ips', default='10.0.0.1')
    parser.add_option('--ir', dest='ipr', default='10.0.0.3')
    (options, args) = parser.parse_args()

    port_RtoC = 50001
    port_RtoS_command = 50002
    port_RtoS_contents = 50003

    RtoC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RtoC_socket.bind((options.ipr, port_RtoC))
    RtoC_socket.listen(5)  # max backlog of connections

    RtoS_socket_comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RtoS_socket_comm.connect((options.ips, port_RtoS_command))
    
    RtoS_socket_cont = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RtoS_socket_cont.bind((options.ipr, port_RtoC))
    RtoC_socket.listen(1)  # max backlog of connections

    pid = fork()
    if(pid == 0):
        handle_command(RtoC_socket, RtoS_socket_comm)
    elif(pid > 0):
        handle_contents(RtoS_socket_cont)

if __name__ == '__main__':
    main()