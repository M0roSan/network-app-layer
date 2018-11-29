import socket, optparse

def main():
    parser = optparse.OptionParser()
    parser.add_option('--is', dest='ips', default='127.0.0.1')
    parser.add_option('--ir', dest='ipr', default='127.0.0.1')
    parser.add_option('-c', dest='command', type='int', default='0')
    (options, args) = parser.parse_args()

    port_CtoS = 50000
    CtoS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CtoS_socket.connect((options.ips, port_CtoS))
    logger = open('log_con.txt', 'w')

    CtoS_socket.send('GET REQUEST')
    response = CtoS_socket.recv(4096)
    logger.write(response)
    logger.flush()
    logger.close()

if __name__ == '__main__':
    main()