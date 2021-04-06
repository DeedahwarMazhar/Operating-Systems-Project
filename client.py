from socket import *
import time
import sys

IP = "127.0.0.1"
PORT = 1234
connected = False


def options():
    option = input("Enter your desired option:")
    if (option == "1"):
        file = input("Enter Filename:")
        while (not file.endswith(".txt")):
            file = input("Invalid Filename. Please enter a file name ending with .txt: ")
        mode = input("Enter mode 'a' for append, 'w' for write, 'r' for read:")
        filemsg = file + ' ' + mode

    elif (option == "2" or option == "3" or option == "5" or option == "6"):
        file = input("Enter Filename:")
        while (not file.endswith(".txt")):
            file = input("Invalid Filename. Please enter a file name ending with .txt")
        filemsg = str(file)

    elif (option == '4'):
        file = input("Enter Filename:")
        while (not file.endswith(".txt")):
            file = input("Invalid Filename. Please enter a file name ending with .txt")
        mode = input("Enter mode 'a' for append, 'w' for write:")
        data = input("Enter data to write")
        filemsg = str(file + ' ' + mode + " " + data)

    elif (option == '7'):
        filemsg = ''
    elif (option == '8'):
        filemsg=''
    else:
        print("invalid option")
    optionmsg = str( option + " " + filemsg)
    return optionmsg
def execute_client():
    global PORT
    global IP
    global connected
    
    username = input("Enter a username:")
    ip=input("Enter Server IP address:")

    client_socket = socket(AF_INET, SOCK_STREAM)
    print('Waiting for connection response')

    while True:
        try:
            client_socket.connect((ip, PORT))
            print("connection successful")
            break
        except error as e:
            print("Server unavailable.Trying again in 2 secs...")
            time.sleep(2)


    client_socket.send(("username: " + username).encode())

    while True:
        msg = client_socket.recv(1024)
        msg = msg.decode()
        filemsg = ""
        print(msg)
        optionmsg = options()
        client_socket.sendall(optionmsg.encode())
        if (optionmsg == "8 "):
            time.sleep(3)
            execute_client()
        print("Please wait...")
execute_client()
    
