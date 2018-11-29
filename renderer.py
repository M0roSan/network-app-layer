import socket, optparse
import threading
from os import fork

def handle_controller_connection(controller_socket, RtoS_socket):
    logger = open('log_ren.txt', 'a')
    request = controller_socket.recv(1024)
    logger.write('Received %s\n' % (request))
    controller_socket.send('ACK-renderer')
    RtoC_socket.send(request)
    response = RtoC_socket.recv(4096)
    logger.write(response)
    logger.flush()
    logger.close()
    controller_socket.close()

def handle_controller(RtoC_socket, RtoS_socket):
    while True:
        controller_sock, address = RtoC_socket.accept()
        print 'Accepted connection from {}:{}'.format(address[0], address[1])
        client_handler = threading.Thread(
            target=handle_controller_connection,
            args=(controller_sock,RtoS_socket,)
        )
        client_handler.start()
        



def main():
    parser = optparse.OptionParser()
    parser.add_option('--is', dest='ips', default='127.0.0.1')
    parser.add_option('--ir', dest='ipr', default='127.0.0.1')
    (options, args) = parser.parse_args()

    port_RtoC = 50001
    port_RtoS_command = 50002
    port_RtoS_contents = 50003

    bind_ip_ren = options.ipr

    RtoC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RtoC_socket.bind((bind_ip_ren, port_RtoC))
    RtoC_socket.listen(5)  # max backlog of connections

    RtoS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RtoC_socket.connect((options.ips, port_RtoS_command))
    


    #pid = fork()
    #if(pid == 0):
    #    handle_command(RtoS_socket)
    #elif(pid > 0):
    #    handle_controller(RtoC_socket)
    handle_controller(RtoC_socket, RtoS_socket)
if __name__ == '__main__':
    main()