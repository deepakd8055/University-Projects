from socket import *
import sys
from time import time
from datetime import datetime

def establish_connection(server_IP, server_port):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_IP, server_port))
    return client_socket

def send_recv_message(client_socket, buffer_size):
    exitMsg = ""
    covert_bin = ""
    one = 0.095
    zero = 0.01
    DEBUG = True
    print("Message is:")
    tMsg = ""
    tDiff = []
    exitMsg = client_socket.recv(buffer_size).decode()
    #Receive messages from server and calculate the time gap between mesgs received
    while exitMsg.rstrip("\n") != "EOF":
        sys.stdout.write(exitMsg)
        sys.stdout.flush()
        t0 = time()
        exitMsg = client_socket.recv(buffer_size).decode()
        t1 = time()
        timeDiff = round(t1-t0, 3)
        tDiff.append(timeDiff)
    sys.stdout.write(exitMsg)
    sys.stdout.flush()
    print()
    #Identify different times and assign 1 or 0 to each time gap
    if DEBUG == True:
        print(tDiff)
        pass
    for timeDiff in tDiff:
        if timeDiff >= one:
            covert_bin += "1"
        elif timeDiff >= zero:
            covert_bin += "0"
    exitMsg = ""
    #convert binary to string value
    for i in range(0,len(covert_bin),8):
        if i+8 <= len(covert_bin):
            exitMsg += chr(int(covert_bin[i:i+8],2))
        else:
            exitMsg += chr(int(covert_bin[i:],2))
    client_socket.close()
    print("\n[disconnect from the chat server]")
    sys.stdout.write("Covert message: "+exitMsg)
    print()

print("[connect to the chat server]")
client_socket = establish_connection("192.168.0.63",12003)    
#client_socket = establish_connection("138.47.98.190",31337)
print("[connection established]")

#receive messages from the Server here
send_recv_message(client_socket, 2048)



