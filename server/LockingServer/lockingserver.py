import socket
from thread import *
import threading
import os

class LockingServer():

    def __init__(self, name, port=8002, host="0.0.0.0", max_threads=3):
        self.port = port
        self.name = name
        self.host = host
        self.semaphore = threading.BoundedSemaphore(value=max_threads)
        self.locked={}


    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(1)
        print "Locking Server: {}, {}:{}".format(self.name,self.host,self.port)

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
            if command == "PING":
                response = "OK: NAME={} HOST={} PORT={} Locking Server".format(self.name, self.host, self.port)
            elif command == "LOCK":
                filename = parameters.split(" ")[0].split("=")[1]
                secs = parameters.split(" ")[1].split("=")[1]

                print "LOCKING {}".format(filename)
                if filename in self.locked:
                    response = "ERROR: File already locked".format(self.files[filename])
                else:
                    self.locked[filename] = secs
                    response = "OK: {} locked for {} sec".format(filename, secs)

            elif command == "UNLOCK":
                filename = parameters.split(" ")[0].split("=")[1]

                print "UNLOCKING {}".format(filename)
                if filename  not in self.locked:
                    response = "OK: {} already unlocked".format(filename)
                else:
                    del(self.locked[filename])
                    response = "OK: {} unlocked".format(filename)

            elif command == "CHECK":
                filename = parameters.split(" ")[0].split("=")[1]
                print "CHECKING {}".format(filename)
                if filename  in self.locked:
                    response = "OK: {} is locked".format(filename)
                else:
                    response = "OK: {} is not locked".format(filename)
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
