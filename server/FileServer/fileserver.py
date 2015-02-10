import socket
from thread import *
import threading
import os
from FileServer.nfs import FileServer


class FileServer():

    def __init__(self, name, port=8000, host="0.0.0.0", directoryServer=0, max_threads=3):
        self.port = port
        self.name = name
        self.host = host
        self.directoryServer = directoryServer
        self.fileLoc = "~/distributedFileServer/"
        self.semaphore = threading.BoundedSemaphore(value=max_threads)
        self.fileLoc = os.path.expanduser(self.fileLoc)


    def run(self):
        if not os.path.exists(self.fileLoc):
            os.makedirs(self.fileLoc)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        print "listening"

        while(1):
            conn, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            self.semaphore.acquire()
            start_new_thread(self.process, (conn,))

    def process(self, conn):
        keepalive = True
        processfiles = FileServer(self.fileLoc)
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
            elif command == "CREATE":
                response = processfiles.CREATE(parameters)
            elif command == "REMOVE":
                response = processfiles.REMOVE(parameters)
            elif command == "WRITE":
                response = processfiles.WRITE(parameters)
            elif command == "READ":
                response = processfiles.READ(parameters)
            elif command == "MKDIR":
                response = processfiles.MKDIR(parameters)
            elif command == "RMDIR":
                response = processfiles.RMDIR(parameters)
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