# DHCP Server
import socket
import sys
import operator
import list_all_ip as lip
import os
addr = ('', 33333)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDPSock.bind(addr)

try:
    #read the file
    file = open("s.conf", "r")
    count = 0
    count_Machines=0
    total_Machines=0
    cidr=0
    current_cidr=0
    current_subnet=0
    server=''
    Machines=[]
    N=0
    allocated_Macs=[]
    Labs=[]
    server_cidr = '0.0.0.0'
    for line in file:

        count += 1
        if count == 1:
            #IP CIDR format

            line = lip.first(line.split('/')[0], line.split('/')[1]) + '/' + line.split('/')[1]
            #server=line.split('/')[0]

            cidr=int(line.split('/')[1])
            server_cidr = line
            #server_cidr=lip.next(server_cidr.split('/')[0])+'/'+str(cidr)
            #os.system('ifconfig enp4s0 '+(server_cidr.split('/')[0])+'/'+str(cidr))
            # print 'ifconfig enp4s0 '+(server_cidr.split('/')[0])+'/'+str(cidr)
            total_Machines=1<<(32-cidr)
        elif count==2:
            N=int(line)
        elif count <= N+2:
            Labs.append((line.split(':')[0],int(line.split(':')[1])+3))
            count_Machines+=int(line.split(':')[1])+3
        else:
            Machines.append((line.split(' ')[0],line.split(' ')[1].rstrip('\n')))
    #Labs.append(('Other',total_Machines-count_Machines))
    
    Labs.sort(key=operator.itemgetter(1),reverse=True)

    VLSM=lip.allot_cidr(server_cidr,Labs)

    Allocation=[]
    i=0
    for subnet in VLSM:
        # 0-lab 1-cidr 2-list 2-network 2-broadcast
        if len(subnet[2])==0:
            Allocation.append((subnet[0],subnet[1],subnet[2],[],[],[]))
            i+=1
            continue

        Allocation.append((subnet[0],subnet[1],subnet[2],subnet[2][0],subnet[2][len(subnet[2])-1],subnet[2][1],subnet[2][1]))
        Allocation[i][2].pop(0)
        Allocation[i][2].pop(0)
        Allocation[i][2].pop(len(Allocation[i][2])-1)
        i+=1
    alloc_server=0
    for lab in Allocation:
        if lab[0]=='Other' and len(lab[2])>0:
            alloc_server=1
            server=lab[2].pop(0)
            print 'ha1'

    if alloc_server==0:
        for lab in Allocation:
            for Lab in Labs:
                if lab[0]==Lab[0] and Lab[1]-3<len(lab[2]):

                    alloc_server=1
                    server=lab[2].pop(0)

                    break
            if alloc_server:
                break



    if alloc_server==0:
        for lab in Allocation:
            if len(lab[2])>0:
                alloc_server=1
                server=lab[2].pop(0)
                print 'ha3'
                break

    print "Server IP: ",server





    # Receive messages
    while True:
        data, addr = UDPSock.recvfrom(1024)
        mac=data
        lab=''
        for machine in Machines:
            if data==machine[0]:
                lab=machine[1]
        if lab=='':
            lab='Other'
        data=''
        i=0
        for Lab in Allocation:
            if mac in allocated_Macs:
                data='IP was already allocated to this Machine'
                out='IP was already allocated to'
                break
            if lab==Lab[0]:

                if len(Lab[2])==0:
                    print lab
                    data='NO IPs Available'
                    out='NO IPs Available to allocate to'
                    break
                data+=Allocation[i][2][0]+'/'+Allocation[i][1].split('/')[1]+'\n'
                Allocation[i][2].pop(0)
                data+=Allocation[i][3]+'\n'
                data+=Allocation[i][4]+'\n'
                data+=Allocation[i][5]+'\n'
                data+=Allocation[i][5]
                out="Allocation Successful to MAC Address"
                allocated_Macs.append(mac)
                break
            i+=1

        print out,mac
        UDPSock.sendto(data, addr)

except KeyboardInterrupt:
    # quit
    UDPSock.close()
    print 'Server stopped.'
    sys.exit()
