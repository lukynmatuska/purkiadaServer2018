# -*- coding: utf-8 -*-
def openFile(i=0, name="server", ext=".log"):
    try:
        file = open(name+i+ext, "r")
        file.close()
        openFile(i+1)
    except:
        file = open(name+str(i)+ext, "w")
        print("Log file name: {}".format(name+str(i)+ext))
        return file

log1 = openFile()
# část kodu pro komunikaci se servrem není potřeba teď řešit
import sys
import socket
import threading
path = "home/"  # ukazatel kde jsem v jaké složce


class User():
    def __init__(self, path, home, name) :
        self.name = name
        self.path = path  #aktualni cesta? :/
        self.actualPath = "home/"
        self.dirIndex = 0 #nova self.pom
        self.action = ""
        self.argv = ""
        self.home = home
        self.a = "" #k cemu to je? :(

    def get_target_dir(self, path):
        directory = self.home
        dirs = path.split("/")
        dirsLs = dirs
        print("dirs: {}".format(dirs))
        for str in dirs:
            for object in home.content:
                if str == object:
                    print("Str: {} Object:{}".format(str, object))
        print("Directory name: {}".format(directory.name))
        print("self.dirIndex: {}".format(self.dirIndex))
        path2 = self.path.split("/")
        del path2[-1]

        if self.action == "exit":
            exit()

        if directory.name != path2[-1]:
            for i in directory.content:#files:
                if i.atribute == "directory":
                    if i.name == path2[self.dirIndex+1]:
                        print("len(path2)): {}".format(len(path2)))
                        if self.dirIndex < len(path2):
                            self.dirIndex += 1
                        self.get_target_dir(i)


        elif directory.name == path2[-1]:
            if self.action == "cd":
                if self.argv == "..":
                    if self.dirIndex != 1:
                        self.dirIndex -= 1
                if self.argv == "/":
                    self.dirIndex = 1
                #self.a = directory.cd(self.argv, self.path)
                self.path = directory.cd(self.argv, self.path)
                """if self.argv in self.a:
                    self.dirIndex += 1"""

            if self.action == "ls":
                #self.a = directory.ls(self.a)
                self.a = directory.lsNew(self.path, dirsLs)
            
    def run(self, action):
        self.action = action
        self.action = self.action.split(" ")
        if len(self.action) > 1:
            self.argv = self.action[1]
            self.action = self.action[0]
        else:
            self.action = self.action[0]
            self.argv = None
        self.dirIndex = 0
        self.get_target_dir(self.path)#home)
        #pom = self.a
        print("self.dirIndex: {}".format(self.dirIndex))
        #print(pom)
        return self.a #pom
    #def 


class Directory():  # tvorba složky chyba by neměla být tady
    def __init__(self, name):
        self.name = name
        self.atribute = "directory"
        self.content = [] #byvaly self.files

    def __str__(self):
        return self.name
    
    def add(self, newContent):
        self.content.append(newContent)

    def cd(self, argv, path):
        if argv == "..":
            self.dirs = path.split("/")
            del self.dirs[-1]
            if len(self.dirs) != 1:
                del self.dirs[-1]
            path = ""
            for directoryName in self.dirs:
                path += "{}/".format(directoryName)
            return path
        elif argv == "/":
            self.dirs = path.split("/")
            return pom2[0] + "/"
        else:
            for content in self.content:
                if content.atribute == "directory":
                    if content.name == argv:
                        path += "{}/".format(argv)
            return path

    def ls(self, path):
        self.path = path #rekurze
        print("self.path: {}".format(self.path))
        self.objects = []
        self.dirList = self.path.split("/") #aktualni cesta
        self.dirs = ""
        for content in self.content:
            print("Object: {}".format(content))
            #for content2 in content.content:
                #print("Object2: {}".format(content2))#object))
            self.objects.append(content)#object)
            self.dirs += "{}\n".format(str(content))#object))
        return self.dirs

    def lsNew(self, path, pathStrList):
        self.strDirs = ""
        self.objects = []
        self.path = path #rekurze
        print("self.path: {}".format(self.path))
        self.dirList = self.path.split("/") #aktualni cesta
        if pathStrList[-1] == "":
            del pathStrList[-1]
        for str in pathStrList:
            print("str: {}".format(str))
            for content in self.content:
                print("content: {}".format(content))
                if str == content:
                    self.strDirs += "{}\n".format(str(content))
                    print(True)
        """for content in self.content:
            print("Object: {}".format(content))
            #for content2 in content.content:
                #print("Object2: {}".format(content2))#object))
            self.objects.append(content)#object)
            self.strDirs += "{}\n".format(str(content))#object))"""
        return self.strDirs
        

class File():  # to stejné akorát se souborem
    def __init__(self, name, content):
        self.atribute = "file"
        self.name = name
        self.content = content

    def show_content(self):
        return self.content


# vytvářím složky a dávám je do sebe
users = Directory("users")
data = Directory("data")
data.add(users)

desktop = Directory("desktop")


logs = Directory("logs")
logs.add(users)

root = Directory("root")
root.add(logs)
root.add(desktop)

bin = Directory("bin")
bin.add(data)

home = Directory("home")
home.add(bin)
home.add(root)
home.add(logs)
home.add(data)


f1 = File("text.txt", "hello world")

soc = socket.socket()
if len(sys.argv) > 1:
    soc.bind(("0.0.0.0", int(sys.argv[1])))
else:
    soc.bind(("0.0.0.0", 9600))
name = soc.getsockname()
log1.write("Server successfully started on {}:{}".format(name[0], name[1]))
print("Server successfully started on {}:{}".format(name[0], name[1]))
soc.listen(1)


def one_user(c, a):
    user = User(path, home, "Random name for testing")
    #print("path.encode(): {}".format(path.encode()))
    c.send(path.encode())
    while True:
        action = c.recv(1024).decode("utf8")
        if action != "disconnect":
            user.a = "None"
            answ = user.run(action)
            if action != "exit":
                c.send(answ.encode())
        else:
            c.close()
            log1.close()


while True:
    c, a = soc.accept()
    #print(a)
    print("New client from {}:{}".format(a[0], a[1]))
    cThread = threading.Thread(target=one_user, args=(c, a))
    cThread.daemon = True
    cThread.start()
input("..")
log1.close()

