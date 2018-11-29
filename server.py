import socket, optparse
import threading

def handle_controller_connection(controller_socket):
    request = controller_socket.recv(1024)
    print 'Received {}'.format(request)
    controller_socket.send('ACK!')
    controller_socket.close()

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

    while True:
        controller_sock, address = StoC_socket.accept()
        print 'Accepted connection from {}:{}'.format(address[0], address[1])
        client_handler = threading.Thread(
            target=handle_controller_connection,
            args=(controller_sock,)
        )
        client_handler.start()

if __name__ == '__main__':
    main()