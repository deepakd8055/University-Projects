from socket import *
import sys
from time import *

def create_socket():
    client_socket = socket(AF_INET, SOCK_DGRAM)
    return client_socket

def send_message(client_socket, message, server_IP, server_port):
    client_socket.sendto(message.encode(), (server_IP, server_port))
    return
                         
def recv_message(client_socket, buffer_size):
    received_message, address = client_socket.recvfrom(buffer_size)
    return received_message.decode()    

client_socket = create_socket()
client_socket.settimeout(1)

no_of_messages = int(sys.argv[3])
server_IP = sys.argv[1]
server_port = int(sys.argv[2])
counter = 0
total = 0.0
mini = 0.0
maxi = 0.0
minBool = False
print("Pinging "+server_IP+":")
for count in range(1,no_of_messages+1):
    tim = strftime("%a %b %d %H:%M:%S %Y", gmtime())
    mesg = "Ping "+str(count)+" "+tim
    start = time()
    send_message(client_socket, mesg, server_IP, server_port)
    ttl = int(client_socket.gettimeout())
    try:
        received_message = recv_message(client_socket, 2048)
        lapsedTime = round((time()-start)*1000)
        mesg = "Reply from "+server_IP+": "+received_message+" time="+str((lapsedTime))+"ms TTL="+str(ttl)
        print(mesg)
        counter += 1
        total += lapsedTime
        if minBool == False:
            mini = lapsedTime
            maxi = lapsedTime
            minBool = True
        elif lapsedTime<mini:
            mini = lapsedTime
        elif lapsedTime>maxi:
            maxi = lapsedTime
    except:
        print("Request timed out")
lossperc = round((no_of_messages-counter)*100/float(no_of_messages),2)
print("\nPing statistics for "+server_IP+":\n    Segments: Sent: "+str(no_of_messages)+", Received: "+str(counter)+", Lost: "+str(no_of_messages-counter)+" ("+str(lossperc)+"% Loss)")
if counter == 0:
    counter = 1
print("Approximate round trip times in ms:\n    Minimum = "+str(mini)+"ms, Maximum = "+str(maxi)+"ms, Average = "+str(round(total/(counter),2))+"ms")  
client_socket.close()
