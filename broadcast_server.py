# DHCP Server
import socket
import sys

addr = ('', 33333)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDPSock.bind(addr)

try:
    #read the file
    file = open("subnets.conf", "r")
    count = 0
    server_ip = '0.0.0.0'
    for line in file:
        count += 1
        if count == 1:
            #IP CIDR format
            server_ip = line

    # Receive messages
    while True:
        data, addr = UDPSock.recvfrom(1024)
        print "From addr: '%s', msg: '%s'" % (addr[0], data)
        UDPSock.sendto(data, addr)

except KeyboardInterrupt:
    # quit
    UDPSock.close()
    print 'Server stopped.'
    sys.exit()
