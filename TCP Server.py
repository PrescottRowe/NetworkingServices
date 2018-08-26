#Prescott Rowe
#8/25/2018
#Simple TCP Server, core functionality for a quick and dirty tool that WORKS
import socket
import threading

bind_ip = "0.0.0.0" #Server, so 0.0.0.0 is a placeholder for all IPv4 addresses on local machine
bind_port = 9999

#AF_INET: is for ipv4. SOCK_STREAM: sets up for a TCP stream
TCP_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the TCP server to specified port and ip
TCP_server.bind((bind_ip,bind_port))

#listens witha set Max backlog of connections
TCP_server.listen(5)
print("Service is listening on %s:%d" % (bind_ip, bind_port))

#Thread for client connection
def handle_client(client_socket):
    #prints out data from the client packets
    client_message = client_socket.recv(1024)
    print( "Received packets: %s" % client_message)

    client_socket.send("ACK!")              #Send out an ACK when received
    client_socket.shutdown(socket.SHUT_RDWR)# SHUT_RD Stops further receives from happening
                                            # _WR Stops further sends and _RDWR stops both
    client_socket.close()                   #Its nice to be nice

while True:
    client_socket , addr = TCP_server.accept()#now waits for incoming connection
    print("Connection made from: %s:%d" % (addr[0],addr[1]))
    #calls to threaded fuction to handle incoming data
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()


