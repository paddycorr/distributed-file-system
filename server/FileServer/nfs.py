import os
class FileServer():

    def __init__(self, fileLoc):
        self.fileLoc = fileLoc


    def CREATE(self, request):
        print "Performing CREATE"
        response = ""
        filename = request.split(" ")[0].split("=")[1]

        dirname = os.path.dirname(filename)
        if os.path.exists(self.fileLoc+dirname):
            if os.path.exists(self.fileLoc+filename):
                response = "ERROR: file \"{}\" already exists".format(filename)
            else:
                open(self.fileLoc+filename, 'a').close()
                response = "OK: file \"{}\" created".format(filename)
        else:
            response = "ERROR: directory \"{}\" does not exist".format(dirname)
        return response

    def REMOVE(self, request):
        print "Performing REMOVE"
        filename = request.split(" ")[0].split("=")[1]
        response = ""
        if os.path.exists(self.fileLoc+filename):
            if os.path.isdir(self.fileLoc+filename):
                response = "ERROR: {} is a directory".format(filename)
            else:
                os.remove(self.fileLoc+filename)
                response = "OK: {} removed".format(filename)
        else:
            response = "ERROR: filename \"{}\" does not exist".format(filename)
        return response

    def WRITE(self, request):
        print "Performing WRITE"
        response = "ERROR: Write failed"
        request = request.split(" ", 2)
        print request
        if len(request) is not 3:
            response = "ERROR: Incorrect command"

        filename = request[0].split("=")[1]
        offset = int(request[1].split("=")[1])
        content = request[-1].split("=", 1)[-1]


        if self.__fileExists(self.fileLoc+filename):
            print "opening file"
            file = open(self.fileLoc+filename, "w")
            file.seek(offset)
            file.write(content)
            file.close()
            response = "OK: Write completed"
        else:
            response = "ERROR: {} does not exist".format(filename)

        return response

    def READ(self, request):
        print "Performing READ"
        response = "ERROR: READ failed"

        request = request.split(" ", 2)
        if len(request) is not 3:
            response = "ERROR: Incorrect command"
        filename = request[0].split("=")[1]
        offset = int(request[1].split("=")[1])
        count = int(request[2].split("=")[1])

        if self.__fileExists(self.fileLoc+filename):
            file = open(self.fileLoc+filename, "r")
            file.seek(offset)
            read = file.read(count)
            file.close()
            response = "OK: \n{}".format(read)


        return response

    def MKDIR(self, request):
        print "Performing MKDIR"
        response = ""
        filename = request.split(" ")[0].split("=")[1]

        dirname = os.path.dirname(filename)
        if os.path.exists(self.fileLoc+dirname):
            if os.path.exists(self.fileLoc+filename):
                response = "ERROR: directory \"{}\" already exists".format(filename)
            else:
                os.mkdir(self.fileLoc+filename)
                response = "OK: directory \"{}\" created".format(filename)
        else:
            response = "ERROR: directory \"{}\" does not exist".format(dirname)
        return response

    def RMDIR(self, request):
        print "Performing RMDIR"
        filename = request.split(" ")[0].split("=")[1]
        response = ""
        if os.path.exists(self.fileLoc+filename):
            os.rmdir(self.fileLoc+filename)
            response = "OK: {} removed".format(filename)
        else:
            response = "ERROR: directory \"{}\" does not exist".format(filename)
        return response

    def RENAME(self, filename, newfilename):
        pass

    def __fileExists(self, filename):

        if os.path.exists(filename):
            return True
        return False