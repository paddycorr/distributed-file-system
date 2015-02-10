import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '0.0.0.0'
PORT = 8000

s.connect((HOST, PORT))

while 1: 
    message = raw_input("Say something?\n")
    s.send(message)
    response = s.recv(1024)
    print response
    

s.close()


