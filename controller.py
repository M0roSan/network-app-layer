#!/usr/bin/python
import sys
import socket, optparse
import json
from message import Message


def get_files(message):
    """returns string file name retrieved from message"""
    message_deserialized = json.loads(message)
    filename = message_deserialized['contents'] #returns unicode
    return str(filename)

def main():
    parser = optparse.OptionParser()
    parser.add_option('--is', dest='ips', default='10.0.0.1')
    parser.add_option('--ir', dest='ipr', default='10.0.0.3')
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
        if(command == 1):
            CtoS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CtoS_socket.connect((options.ips, port_CtoS))
            message = Message(command=command)
            CtoS_socket.send(message.export())
            response = CtoS_socket.recv(4096)
            message_rec = Message()
            message_rec.decode(response)
            print("Available files are: \n{}".format(message_rec.payload))

        else:
            RtoC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            RtoC_socket.connect((options.ipr, port_RtoC))
            message = Message(command=command, filename=filename)
            RtoC_socket.send(message.export())
            response = RtoC_socket.recv(4096)
            print("Received from rendedrer: {}".format(response))


if __name__ == '__main__':
    main()