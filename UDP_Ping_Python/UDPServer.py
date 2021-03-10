from socket import *

def create_socket(server_port):
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', int(server_port)))
    return server_socket

def recv_message(server_socket, buffer_size):
    message, client_address = server_socket.recvfrom(buffer_size)
    return client_address, message.decode()

def send_message(message, client_address):
    server_socket.sendto(message.encode(), client_address)
    return

server_port = input("Please, enter UDP connection port number: ")
server_socket = create_socket(server_port)
print("The server is ready to receive messages...\n")

counter = 0
while (True):
    client_address, message = recv_message(server_socket, 2048)
    counter+=1
    print("Received message: {}".format(message))
    if(counter%3 !=0):
        send_message(message, client_address)
        print("Message sent\n")
    else:
        print("Reply not sent\n")
