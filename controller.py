#!/usr/bin/python
import sys
import socket, optparse
import json

def message_request(command, filename=None, contents=None):
    """Create message: JSON like object"""
    message = {'filename': filename, 'request': command, 'contents': contents}
    message_serialized = json.dumps(message)
    return message_serialized

def main():
    parser = optparse.OptionParser()
    parser.add_option('--is', dest='ips', default='127.0.0.1')
    parser.add_option('--ir', dest='ipr', default='127.0.0.1')
    parser.add_option('-c', dest='command', type='int', default='0')
    parser.add_option('-f', dest='filename', default='sample.txt')
    (options, args) = parser.parse_args()

    port_CtoS = 50000
    port_RtoC = 50001
   
    command = options.command
    filename = options.filename

    if not(command == 1 or command == 2 or command == 3 or command == 4 or command == 5):
        print('ERROR REQUEST TYPE. PLEASE TYPE NUMBER FROM 1 to 5. \n e.g.) python controller.py -c 3\n')
        sys.exit()
    else:
        logger = open('log_con.txt', 'a')

        if(command == 1):
            CtoS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CtoS_socket.connect((options.ips, port_CtoS))
            message = message_request(command)
            CtoS_socket.send(message)
            response = CtoS_socket.recv(4096)
            logger.write(response)
            logger.flush()
            logger.close()
        else:
            RtoC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            RtoC_socket.connect((options.ipr, port_RtoC))
            message = message_request(command)
            RtoC_socket.send(message)
            response = RtoC_socket.recv(4096)
            logger.write(response)
            logger.flush()
            logger.close()

if __name__ == '__main__':
    main()