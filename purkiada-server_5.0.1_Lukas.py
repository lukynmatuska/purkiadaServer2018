
# část kodu pro komunikaci se servrem není potřeba teď řešit
import sys
import socket
import threading
path= "home/"  # ukazatel kde jsem v jaké složce


class every_user():
    def __init__(self, path, home,a) :
        self.path = path
        self.pom = 0
        self.action= ""
        self.argv = ""
        self.home = home
        self.a = a

    def get_target_dir(self, directory):
        print(directory.name)
        print(self.pom)
        path2 = self.path.split("/")
        del path2[-1]
        if self.action == "exit":
            exit()

        if directory.name != path2[-1]:
            for i in directory.files:
                if i.atribute == "directory":
                    if i.name == path2[self.pom+1]:
                        print(len(path2))
                        if self.pom < len(path2):
                            self.pom += 1
                        self.get_target_dir(i)


        elif directory.name == path2[-1]:
            if self.action == "cd":
                if self.argv == "..":
                    if self.pom != 1:
                        self.pom -= 1
                if self.argv == "/":
                    self.pom = 1
                self.a = directory.cd(self.argv, self.path)
                """if self.argv in self.a:
                    self.pom += 1"""

            if self.action == "ls":
                self.a= directory.ls(self.a)

    def run(self, action):
        self.action = action
        self.action = self.action.split(" ")
        if len(self.action) > 1:
            self.argv = self.action[1]
            self.action = self.action[0]
        else:
            self.action = self.action[0]
            self.argv = None
        self.pom = 0
        self.get_target_dir(self.home)
        pom = self.a
        print("__ self.pom: {}".format(self.pom))
        print("__ pom: {}".format(pom))
        self.path = pom
        return pom


class Directory():  # tvorba složky chyba by neměla být tady
    def __init__(self, name):
        self.atribute = "directory"
        self.files = []
        self.name = name

    def __str__(self):
        return self.name

    def cd(self, argv, path):
        if argv == "..":
            pom2 = path.split("/")
            del pom2[-1]
            if len(pom2) != 1:
                del pom2[-1]
            path = ""
            for i in pom2:
                path = path + i + "/"
            return path
        elif argv == "/":
            pom2 = path.split("/")
            return pom2[0] + "/"
        else:
            for i in self.files:
                if i.atribute == "directory":
                    if i.name == argv:
                        path += argv + "/"
            return path

    def add(self, file):
        self.files.append(file)

    def lsOLD(self, a):
        dir = ""
        for i in self.files:
            dir += i.name + " "
        return dir
    def ls(self, path):
        self.path = path #rekurze
        print("self.path: {}".format(self.path))
        self.objects = []
        self.dirList = self.path.split("/") #aktualni cesta
        self.dirs = ""
        for content in self.files:#content:
            print("Object: {}".format(content))
            #for content2 in content.content:
                #print("Object2: {}".format(content2))#object))
            self.objects.append(content)#object)
            self.dirs += "{}\n".format(str(content))#object))
        return self.dirs

class File():  # to stejné akorád se souborem
    def __init__(self, name, content):
        self.atribute = "file"
        self.name = name
        self.content = content

    def show_content(self):
        return self.content


# vytvářím složky a dávám je do sebe
home = Directory("home")
bin = Directory("bin")
data = Directory("data")
desktop = Directory("desktop")
users = Directory("users")
logs = Directory("logs")

desktop.add(users)

bin.add(data)
logs.add(users)
root = Directory("root")
root.add(logs)
root.add(desktop)
home.add(bin)
home.add(root)
f1 = File("text.txt", "hello world")

soc = socket.socket()
if len(sys.argv) > 1:
    soc.bind(("0.0.0.0", int(sys.argv[1])))
else:
    soc.bind(("0.0.0.0", 9600))
name = soc.getsockname()
print(name[0], name[1])
soc.listen(1)


def one_user(c, a):
    user = every_user(path, home, "")
    c.send(path.encode())
    while True:
        action = c.recv(1024).decode("utf8")
        if action != "disconect":
            user.a = "None"
            answ = user.run(action)
            c.send(answ.encode())
        else:
            c.close()


while True:
    c, a = soc.accept()
    print(a)
    cThread = threading.Thread(target=one_user, args=(c, a))
    cThread.daemon = True
    cThread.start()
input()







