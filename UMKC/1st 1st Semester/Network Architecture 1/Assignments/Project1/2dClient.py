"""Chat room"""
#2dClient.py

import socket
import select
import sys

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.settimeout(2)
HOST = 'Server.Project1-Oct26.ch-geni-net.instageni.rnet.missouri.edu'
PORT = 9099
BUFFER = 1024
#USER = input("What username do you want? ")
try:
    c.connect((HOST, PORT))
    #c.send(bytes(USER, 'utf-8'))
except:
    print("Unable to connect")
    sys.exit()

SOCK_LIST = [c, sys.stdin]
print("Entered chat room.")
print("To leave chat, type 'quit'")
while 1:
    cRead, cWrite, cError = select.select(SOCK_LIST, [], [])
    for sock in cRead:
        if sock == c:
            # incoming message from remote server
            data = sock.recv(BUFFER)
            if not data:
                print("Disconnected from chat server")
                c.close()
                sys.exit()
            else:
                #Message form another client
                print("{0}".format(data.decode('utf-8')))     
        else:
            # user entered a message
            msg = sys.stdin.readline().splitlines() #stdin adds \EOF as it is used as file operator. splitline used to seperate the orig text from \EOF
            if msg[0].lower() == 'quit':
                print("Leaving chat.")
                c.close()
                sys.exit()
            c.send(bytes(msg[0], 'utf-8'))
c.close()