# Client program

import socket
import sys
import re, uuid

UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create socket
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
addr = ('<broadcast>', 33333)

if len(sys.argv) > 1 and sys.argv[1] == '-m':
    mac_addr = sys.argv[2]
else:
    mac_addr = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

data = mac_addr

if UDPSock.sendto(data, addr):
    data, addr = UDPSock.recvfrom(1024)
    print "%s" % (data)

UDPSock.close()
