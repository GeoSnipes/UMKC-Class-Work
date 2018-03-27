#2dServer.py

import socket
import select

#function to send out message to all clients except the sender
def broadcast(sock, message):
    for sockL in SOCK_LIST:
        if sockL != server and sockL != sock:
            try:
                sockL.send(bytes(message, 'utf-8'))
            except:
                #client disconnected during broadcast function
                if sockL in SOCK_LIST:
                    SOCK_LIST.remove(sockL)  
                    broadcast(sock, "{0} disconnected".format(getUserName(sock.getpeername())))
                    delUserName(sock.getpeername())

#add user to dictionary
def addUserName(address, name):
    USERS[address] = name

#get user name from dictionary
def getUserName(address):
    return USERS[address]

#del user from dictionary
def delUserName(address):
    try:
        del USERS[address]
    except:
        pass

HOST = socket.gethostname()
BUFFER = 1024
PORT = 9099
SOCK_LIST = []

#dictionary consisting of list of users
USERS={}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST,PORT))
server.listen(5)

SOCK_LIST.append(server)
print("Chat server started on ", HOST,":",PORT)
while 1:
    #using select select to get all incoming and outcoming requesting without blocking
    sRead, sWrite, sError = select.select(SOCK_LIST,[],[],0)

    for sock in sRead:
        #a new connection to server
        if sock == server:
            cl, addr= server.accept()
            SOCK_LIST.append(cl)                            #add to list of current users in convo
            
            data = cl.recv(BUFFER).decode('utf-8')        #receive user name
            addUserName(cl.getpeername(), data)             #add name to dictionary
            
            print("Client at {0} connected".format(cl.getpeername()))
            broadcast(cl, "{0} connected".format(getUserName(cl.getpeername())))
        
        #message from a client and not a new connection
        else:
            #receive data from client
            data = sock.recv(BUFFER).decode('utf-8')
            if data:
                #client sent a message
                broadcast(sock, "{0}: {1}".format(getUserName(sock.getpeername()), data)) 
            else:
                #empty message, client sent nothing, client disconnected
                if sock in SOCK_LIST:
                    SOCK_LIST.remove(sock)
                    print("Client at {0} disconnected".format(sock.getpeername()))
                    broadcast(sock, "{0} disconnected".format(getUserName(sock.getpeername())))
                    delUserName(sock.getpeername())
server.close()