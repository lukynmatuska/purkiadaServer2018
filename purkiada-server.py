# -*- coding: utf-8 -*-
# část kodu pro komunikaci se servrem není potřeba teď řešit
import sys
import socket
import threading
path = "home/"  # ukazatel kde jsem v jaké složce


class User():
    def __init__(self, path, home, name) :
        self.name = name
        self.path = path  #aktualni cesta? :/
        self.dirIndex = 0 #nova self.pom
        self.action = ""
        self.argv = ""
        self.home = home
        self.answerToUser= "" #k cemu toje? :(
        self.pathList = [self.home] #"""objekt aktuální složky, resp. poslední složky v cestě"""
        
    def __str__(self):
        return self.name

    def get_target_dir(self, directory):
        print("directory.name: {}".format(directory.name))
        print("self.dirIndex: {}".format(self.dirIndex))
        path2 = self.path.split("/")
        print("path2: {}".format(path2))
        del path2[-1]
        print("path2: {}".format(path2))

        if self.action == "exit":
            exit()

        if self.action == "test":
            print("test")

        if directory.name != path2[-1]:
            for i in directory.files:
                if i.atribute == "directory":
                    if i.name == path2[self.dirIndex+1]:
                        print("len(path2): {}".format(len(path2)))
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
                print("self.path before CD: {}".format(self.path))
                self.pathList, self.answerToUser= directory.cd(self.argv, self.path, self.pathList)
                print("self.answerToUserafter CD: {}".format(self.answerToUser))
                print("self.pathListafter CD: {}".format(self.pathList))
                """if self.argv in self.a:
                    self.dirIndex += 1"""

            if self.action == "ls":
                self.answerToUser= directory.ls(self.pathList[-1])#self.a)
                #self.answerToUser= directory.ls(dirs[-1])
                

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
        self.get_target_dir(self.home)
        #pom = self.a
        #print("self.dirIndex: {}".format(self.dirIndex))
        #print(pom)
        return self.answerToUser#pom
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

    def cd(self, argv, path, pathList):
        if argv == "..":
            #path2 = ""
            #for directoryObject in pathList:
                #path2 += "{}/".format(directoryObject.name)
            #print("pathLis: {}".format(path2))#List))
            #print("pathLis: {}".format(pathList))
            dirs = path.split("/")
            del dirs[-1]
            del pathList[-1]
            if len(dirs) != 1:
                del dirs[-1]
                del pathList[-1]
            path = ""
            for directoryName in dirs:
                path += "{}/".format(directoryName)
            #path2 = ""
            #for directoryObject in pathList:
                #path2 += "{}/".format(directoryObject.name)
            #print("pathLis: {}".format(path2))#List))
            return pathList, path
        elif argv == "/":
            dirs = path.split("/")
            return pathList[0], pom2[0] + "/"
        else:
            for dir in self.content:
                if dir.atribute == "directory":
                    if dir.name == argv:
                        path += "{}/".format(argv)
                        pathList.append(dir)
                        print("pathList: {}".format(pathList))
            print("New path in CD: {}/".format(path))
            return pathList, path

    def lsOld(self, a):
        dir = ""
        for i in self.content:
            dir += i.name + " "
        return dir

    def ls(self, lastFolder):#directory):
        print("lastFolder: {}".format(lastFolder.name))
        dirs = ""
        #lastFolder = self
        for content in lastFolder.content:
            dirs += "{}\n".format(content.name)
            print("content.name: {}".format(content.name))
        return dirs

    def lsLukyn(self):#split path a posledni(slozka) ze seznamu projede cyklem :), pak rekurze
        self.dirList = path.split("/")
        print(self.dirList)
        #global home
        for file in self.content:
            if self.dirList[-1] in file:
                for object in file.files:
                    print("Object: {}".format(object))
        self.dirs = ""
        self.objects=[]
        for object in self.content:
            print(object)
            self.objects.append(object)
            self.dirs += "{}\n".format(str(object))
        return self.dirs

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

desktop = Directory("desktop")
desktop.add(users)

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


f1 = File("text.txt", "hello world")

def openFile(i=0, name="server", ext=".log"):
    try:
        s = open(name+i+ext, "r")
        s.close()
        openFile(i+1)
    except:
        s = open(name+str(i+1)+ext, "w")
        return s
        
log1 = openFile()

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

