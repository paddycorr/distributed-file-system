import socket
from thread import *
import threading
import os
import hashlib

class DirectoryServer():

    def __init__(self, name, port=8001, host="0.0.0.0", directoryServer=0, max_threads=3):
        self.port = port
        self.name = name
        self.host = host
        self.semaphore = threading.BoundedSemaphore(value=max_threads)

        self.files={}
        self.FileServers={}

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        print "Directory Server: {}, {}:{}".format(self.name,self.host,self.port)

        while(1):
            conn, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            self.semaphore.acquire()
            start_new_thread(self.process, (conn,))

    def process(self, conn):
        keepalive = True

        while(keepalive):
            data = conn.recv(1024)
            command = data.split(" ", 1)[0]
            if len(data.split(" ", 1)) > 1:
                parameters = data.split(" ", 1)[1]
            else :
                parameters =""

            response = ""
            if command == "NULL":
                response = "OK: NAME={} HOST={} PORT={}".format(self.name, self.host, self.port)
            ### SEARCH FILENAME={filename}
            elif command == "SEARCH":
                print "Performing Search"
                filename = hashlib.md5(parameters.split(" ")[0].split("=")[1])
                if filename in self.files:
                    response = "OK: Found file on {}".format(self.files[filename])
                else:
                    response = "ERROR: File not found"
            elif command == "REGISTERFILE": 
                print "registering file"
                servername = parameters.split(" ")[0].split("=")[1]
                filename = parameters.split(" ")[1].split("=")[1] 
                self.files[filename] = servername
            elif command == "REMOVEFILE":
                print "removing file" 
                filename = parameters.split(" ")[0].split("=")[1] 
                del(self.files[filename])
            elif command == "KILL_SERVICE":
                keepalive=False
                os._exit
            else:
                response = "No handler"
            print "Send response"
            conn.sendall(response)

        conn.close()
        print "leaving thread"
        self.semaphore.release()
        return
