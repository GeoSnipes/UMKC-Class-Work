"""File transfer app"""
#4ExterClientFT.py
import socket

csFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
csFT.connect((socket.gethostname(), 8757))

text_file = 'passphrase.txt'

#Send file
with open(text_file, 'rb') as fs: 
    #Using with, no file close is necessary, 
    #with automatically handles file close
    print('Client Sending file..')
    while True:
        data = fs.read(1024)
        print(data)
        if not data:
            print('break')
            csFT.send(b'EOF')
            break
        print('not in break')
        csFT.send(data)
    print('Client Done Sending File..')

#Receive file
print("Client Receiving Updated File..")
with open(text_file, 'wb') as fw:
    while True:
        data = csFT.recv(1024)
        if data == b'':
            break
        fw.write(data)
print("Client Done Receiving Updated File..")

csFT.close()