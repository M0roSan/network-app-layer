import socket, optparse
import threading
from os import fork
from message import Message

def handle_controller_connection(controller_socket, RtoS_socket):
    request = controller_socket.recv(1024)
    print('Controller: {}\n'.format(request))
    message_con = Message(payload='ACK-renderer')
    controller_socket.send(message_con.export())

    RtoS_socket.send(request)

    message = Message()
    while True:
        response = RtoS_socket.recv(1024)
        if not response:
            break
        #message.decode(response)
        #print(message.payload)
        print(response)
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
    parser.add_option('--is', dest='ips', default='10.0.0.1')
    parser.add_option('--ir', dest='ipr', default='10.0.0.3')
    (options, args) = parser.parse_args()

    port_RtoC = 50001
    port_RtoS = 50002

    #RtoC is server side(server-client relationship)
    RtoC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RtoC_socket.bind(("", port_RtoC))
    RtoC_socket.listen(5)  # max backlog of connections
    #RtoS is client side
    RtoS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RtoS_socket.connect((options.ips, port_RtoS))

    handle_controller(RtoC_socket, RtoS_socket)

if __name__ == '__main__':
    main()
