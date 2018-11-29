import socket, optparse
from os import fork

def handle_controller_connection(controller_socket):
    logger = open('log_ser.txt', 'a')
    request = controller_socket.recv(1024)
    logger.write('Received %s\n' % (request))
    controller_socket.send('ACK-renderer')
    logger.close()
    controller_socket.close()

def handle_controller(RtoC_socket):
    while True:
        controller_sock, address = RtoC_socket.accept()
        print 'Accepted connection from {}:{}'.format(address[0], address[1])
        client_handler = threading.Thread(
            target=handle_controller_connection,
            args=(controller_sock,)
        )
        client_handler.start()

def main():
    parser = optparse.OptionParser()
    parser.add_option('--is', dest='ips', default='127.0.0.1')
    parser.add_option('--ir', dest='ipr', default='127.0.0.1')

    port_RtoC = 50001
    port_RtoS_command = 50002
    port_RtoS_contents = 50003

    bind_ip = options.ipr

    RtoC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RtoC_socket.bind((bind_ip, port_RtoC))
    RtoC_socket.listen(5)  # max backlog of connections

    handle_controller(RtoC_socket)

if __name__ == '__main__':
    main()