#4ExterServerFT.py

import socket

ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssFT.bind((socket.gethostname(), 8757))
ssFT.listen(1)



while True:
    conn, address = ssFT.accept()
    print('Connected to ', address[0], ':', address[1])
    
    text_file = 'fileProj.txt'

    #Receive, output and save file
    with open(text_file, "wb") as fw:
        print("Server Receiving..")
        while True:
            print('receiving')
            data = conn.recv(1024)
            print('Received: ', data.decode('utf-8'))
            if data == b'EOF':
                print('in break')
                break
            #print('Received: ', data.decode('utf-8'))
            print('not in break')
            fw.write(data)
        print("Server Done Receiving..")

    #Append and send file
    print('Server Updating and Sending File..')
    with open(text_file, 'ab+') as fa:
        string = b"\rAppend this to file."
        fa.write(string)
        fa.seek(0, 0)
        while True:
            data = fa.read(1024)
            if not data:
                break
            conn.send(data)
    print('Server Done Updating and Sending File..')
    conn.close() #Disconnect from client