from socket import *
import os
import time

def create_socket(server_port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    return server_socket

def accept_client(server_socket):
    connection_socket, address = server_socket.accept()
    return connection_socket 

#send message to client
def send_message(connection_socket, message):
    connection_socket.send(message)
    return


server_port = 12002
server_socket = create_socket(int(server_port))
print("The server is ready to receive \n")

connection_socket = accept_client(server_socket)
covert_msg = "byeEOF"
Msg = "123123123123123123123123123123123123123123123123"
zero = 0.025
one = 0.1
n = 0
covert_bin = ""
#convert covert message to binary value
for msg in covert_msg:
    covert_bin += format(ord(msg),'#010b')[2:]
print(covert_bin)
#send covert message with time gap based on the 1 or 0 value
for msg in Msg:        
    send_message(connection_socket, msg.encode())
    if covert_bin[n] == "0":
        time.sleep(zero)
    else:
        time.sleep(one)
    n = (n+1)%len(covert_bin)
send_message(connection_socket, "EOF".encode())
connection_socket.close()
time.sleep(one)
