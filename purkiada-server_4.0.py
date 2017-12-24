

# část kodu pro komunikaci se servrem není potřeba teď řešit

import socket
import threading


path="home/" #ukazatel kde jsem v jaké složce
class every_user():
    def __init__(self, path,home,a):
        self.path = path
        self.pom = 1
        self.action=""
        self.argv = ""
        self.home = home
        self.a = a
    def get_target_dir(self,directory):
        path2 = self.path.split("/")
        print(path2)
        del path2[-1]
        if self.action == "cd.." or self.action == "exit":
            if self.action == "cd..":
                self.path=directory.cd__(self.path)
                if self.pom != 1:
                    self.pom -= 1
                return self.path
            if self.action == "exit":
                exit()

        elif directory.name != path2[-1]:
            print(directory.name)
            for i in directory.files:
                if i.atribute == "directory":
                    print(self.pom)
                    if i.name == path2[self.pom]:
                        if self.pom < len(path2)-1:
                            self.pom += 1
                        self.get_target_dir(i)


        print(directory.name)
        if directory.name == path2[-1]:
            if self.action == "cd":
                self.path = directory.cd(self.argv,self.path)
                return "done"
            if self.action == "ls":
                self.a=directory.ls(self.a)
                return "done"
    def run(self,action):
        self.action = action
        self.action = self.action.split(" ")
        if len(self.action) > 1:
            self.argv = self.action[1]
            self.action = self.action[0]
        else:
            self.action = self.action[0]
            self.argv = None
        pom = self.get_target_dir(self.home)
        if self.action == "ls":
            pom = self.a
        if self.action == "cd" or self.action == "cd..":
            pom = self.path
        print(self.path)
        return pom


class Directory(): #tvorba složky chyba by neměla být tady
    def __init__(self,name):
        self.atribute = "directory"
        self.files = []
        self.name = name
    def cd(self,file,path):
        for i in self.files:
            if i.atribute == "directory":
                if i.name == file:
                    path += file + "/"
        return path
    def add(self,file):
        self.files.append(file)
    def ls(self,a):
        dir = ""
        for i in self.files:
            dir += i.name + " "
        return dir
    def cd__(self,path):
        pom2 = path.split("/")
        del pom2[-1]
        if len(pom2) != 1:
            del pom2[-1]
        path = ""
        for i in pom2:
            path=path+i+"/"
        return path
class File(): # to stejné akorád se souborem
    def __init__(self,name,content):
        self.atribute = "file"
        self.name = name
        self.content = content
    def show_content(self):
        return self.content



#vytvářím složky a dávám je do sebe
home=Directory("home")
bin = Directory("bin")
data = Directory("data")
desktop = Directory("desktop")
users = Directory("users")
logs = Directory("logs")

desktop.add(users)

bin.add(data)
logs.add(users)
root=Directory("root")
root.add(logs)
root.add(desktop)
home.add(bin)
home.add(root)
f1=File("text.txt","hello world")






soc = socket.socket()


soc.bind(("0.0.0.0",9600))
name = soc.getsockname()
print(name[0],name[1])
soc.listen(1)

def one_user(c,a):
    user = every_user(path,home,"")
    c.send(path.encode())
    while True:
        action = c.recv(1024).decode("utf8")
        if action != "disconect":
            user.a = "None"
            answ=user.run(action)
            c.send(answ.encode())
        else:
            c.close()
        
while True:
    c,a=soc.accept()
    print(a)
    cThread = threading.Thread(target = one_user, args=(c,a))
    cThread.daemon = True
    cThread.start()
input()







