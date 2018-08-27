#Prescott Rowe
#8/25/2018
#Simple UDP Client, core functionality for a quick and dirty tool that WORKS

import socket

target_host = "127.0.0.1" #local loopback
target_port = 80    #http

#client is a socket object. AF_INET specifies ipv4, SOCK_DGRAM is used for UDP connections
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# host<->port<->target
client.bind((target_host, target_port))

#UDP doesn't care, slam em with data if you want
client.sendto(b'Hey have some data',(target_host, target_port))

#receive response
target_response, addr = client.recvfrom(4096) #can take up to 512 octets of data
client.shutdown(socket.SHUT_RD) # SHUT_RD Stops further receives from happening
                                # _WR Stops further sends and _RDWR stops both
print(target_response)
client.close()                  #release socket, similar to os.close() for sockets

