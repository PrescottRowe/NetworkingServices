#Prescott Rowe
#8/25/2018
#Simple TCP Client, core functionality for a quick and dirty tool that WORKS

import socket

target_host = "www.url.com"   #"www.url.com"  or IP addr
target_port = 80 #http

#client is a socket object. AF_INET: says we are using ipv4. SOCK_STREAM: lets us use a TCP stream
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connects: client <-> port <-> target
client.connect((target_host, target_port))

#Both clients and servers MUST support the Host request-header.
#A client that sends an HTTP/1.1 request MUST send a Host header.
client.send(b'GET / HTTP/1.1\r\nHost: url.com\r\n\r\n')#do not change this formatting unless you understand URI-Request
#Servers MUST report a 400 (Bad Request) error if an HTTP/1.1 request does not include a Host request-header.
#Servers MUST accept absolute URIs.

#A client MUST be prepared to accept one or more 1xx status responses prior to a regular response, even if the
# client does not expect a 100 (Continue) status message. Unexpected 1xx status responses MAY be ignored by a user agent
target_response = client.recv(4096) #allows for 512 octets of data, can be raised but i think is should be enough for the longest http message body
client.shutdown(socket.SHUT_RD) # SHUT_RD Stops further receives from happening
                         # _WR Stops further sends and _RDWR stops both
print(target_response)

client.close() #release socket, similar to os.close() for sockets
