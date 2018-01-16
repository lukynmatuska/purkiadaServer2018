# -*- coding: utf-8 -*-
import sys
import socket
import threading
import time

path = "home/"  # ukazatel kde jsem v jaké složce
users_file = open("users.txt", "r+")
user_names = users_file.readlines()
users_file.close()
print(user_names)

class User():

    def __init__(self, path, home, adress):
        self.name = ""
        self.adress = adress
        self.path = path  # aktualni cesta? :/
        self.connected = False
        self.action = ""
        self.argv = ""
        self.directory = home
        self.answerToClient = ""  # k cemu toje? :(
        self.pathList = [home]  # """objekt aktuální složky, resp. poslední složky v cestě"""
        self.perrmission = "user"
        self.admin_pass = "secret message"
        self.acess = False
    def cd(self):
        self.pathList2 = self.path.split("/")
        if self.argv == "..":
            self.acess = True
            try:
                if len(self.pathList) != 1:
                    del self.pathList[-1]

            except:
                pass
        elif self.argv == "/":
            try:
                self.pathList = self.pathList[0]
                self.acess = True
            except:
                pass
        else:
            for dir in self.directory.content:
                if dir.name == self.argv:
                    if self.perrmission in dir.acess:
                        self.acess = True
                        if dir.atribute == "directory":
                            self.path += "{}/".format(self.argv)
                            try:
                                self.pathList.append(dir)
                            except:
                                pom = []
                                pom.append(self.pathList)
                                pom.append(dir)
                                self.pathList = pom
                    else:
                        self.acess = False



    def __str__(self):
        return self.name


    def use_commands(self):
        try:
            self.directory = self.pathList[-1]
        except:
            self.directory = self.pathList
        if self.action == "exit":
            exit()

        if self.action == "cd":
            self.cd()
            self.path = ""

            if self.argv != "/" and self.directory != self.pathList:
                for i in self.pathList:
                    self.path += i.name + "/"

            else:
                self.path = self.pathList.name+"/"
            self.answerToClient = self.path

        if self.action == "ls":
            self.answerToClient = self.directory.ls()
            self.acess = True

        if self.action == "read":
            self.answerToClient = "None such file"
            for i in self.directory.content:
                if i.name == self.argv:
                    if self.perrmission in i.acess:
                        self.acess = True
                        if i.atribute == "file":
                            self.answerToClient = i.show_content()
                            print(self.answerToClient)
                    else:
                        self.acess = False
                        self.answerToClient = "None such file"
        if self.action == "bcad":
            self.acess = True
            if self.argv == self.admin_pass:
                self.answerToClient = "True"
                self.perrmission = "admin"
            else:
                self.answerToClient = "False"
    def run(self, action):
        self.action = action
        self.action = self.action.split(" ")
        if len(self.action) > 1:
            self.argv = self.action[1]
            self.action = self.action[0]
        else:
            self.action = self.action[0]
            self.argv = None
        self.use_commands()
        return self.answerToClient  # self.pathList##pom

class Directory():  # tvorba složky chyba by neměla být tady
    def __init__(self, name,acess):
        self.name = name
        self.atribute = "directory"
        self.content = []  # byvaly self.files
        self.acess = acess

    def __str__(self):
        return self.name

    def add(self, newContent):
        self.content.append(newContent)

    def ls(self):
        dir = ""
        for i in self.content:
            dir += i.name + " "
        if dir == "":
            dir = "None"
        return dir


class File():  # to stejné akorát se souborem
    def __init__(self, name, content,acess):
        self.atribute = "file"
        self.name = name
        self.content = content
        self.acess = acess

    def show_content(self):
        return "File content: {}".format(self.content)

acess_list = ["user", "admin"]
# vytvářím složky a dávám je do sebe
users = Directory("users",acess_list)
data = Directory("data",acess_list)

desktop = Directory("desktop",acess_list)
desktop.add(users)

logs = Directory("logs",["admin"])
logs.add(users)

root = Directory("root",acess_list)
root.add(logs)
root.add(desktop)

bin = Directory("bin",acess_list)
bin.add(data)


f2 = File("text2.txt", "hello world2",acess_list)

home = Directory("home",acess_list)
home.add(bin)
home.add(root)
home.add(logs)
home.add(f2)

f1 = File("text.txt", "hello world",acess_list)

soc = socket.socket()
if len(sys.argv) > 1:
    soc.bind(("0.0.0.0", int(sys.argv[1])))
else:
    soc.bind(("0.0.0.0", 9800))
name = soc.getsockname()
print(name)
soc.listen(1)
banner2 = r"""
 _______                    __       __                __                  ______   ______    __    ______
/       \                  /  |     /  |              /  |                /      \ /      \ _/  |  /      \
$$$$$$$  |__    __  ______ $$ |   __$$/  ______   ____$$ | ______        /$$$$$$  /$$$$$$  / $$ | /$$$$$$  |
$$ |__$$ /  |  /  |/      \$$ |  /  /  |/      \ /    $$ |/      \       $$____$$ $$$  \$$ $$$$ | $$ \__$$ |
$$    $$/$$ |  $$ /$$$$$$  $$ |_/$$/$$ |$$$$$$  /$$$$$$$ |$$$$$$  |       /    $$/$$$$  $$ | $$ | $$    $$<
$$$$$$$/ $$ |  $$ $$ |  $$/$$   $$< $$ |/    $$ $$ |  $$ |/    $$ |      /$$$$$$/ $$ $$ $$ | $$ |  $$$$$$  |
$$ |     $$    $$/$$ |     $$ | $$  $$ $$    $$ $$    $$ $$    $$ |      $$       $$   $$$// $$   $$    $$/
$$/       $$$$$$/ $$/      $$/   $$/$$/ $$$$$$$/ $$$$$$$/ $$$$$$$/       $$$$$$$$/ $$$$$$/ $$$$$$/ $$$$$$/



"""

banner = r"""
-----------------------------------------------------------------
  _____            _    _           _         ___   ___ __  ___
 |  __ \          | |  (_)         | |       |__ \ / _ /_ |/ _ \
 | |__) _   _ _ __| | ___  __ _  __| | __ _     ) | | | | | (_) |
 |  ___| | | | '__| |/ | |/ _` |/ _` |/ _` |   / /| | | | |> _ <
 | |   | |_| | |  |   <| | (_| | (_| | (_| |  / /_| |_| | | (_) |
 |_|    \__,_|_|  |_|\_|_|\__,_|\__,_|\__,_| |____|\___/|_|\___/

-----------------------------------------------------------------
"""
def one_user(c, a):
    user = User(path, home, a)
    try:
        c.send(banner.encode())
        time.sleep(0.2)
        c.send(path.encode())

        #část kodu, která se změní
        while user.connected == False:
            data = c.recv(1024).decode("utf8")
            user.name = data.split("-")[0]
            for i in user_names:
                if data in i:
                    c.send("True".encode())
                    user.connected = True
            if user.connected == False:
                c.send("False".encode())


                
        while True:
            action = c.recv(1024).decode("utf8")
            userLog = open("/home/hojang/Users_Logs/"+user.name + "_Log.txt", "a")
            userLog.write(action+"\n")
            userLog.close()
            if action != "disconnect":
                user.acess = False
                user.answerToClient = "None"
                answ = user.run(action)
                if user.acess == True:
                    c.send("True".encode())
                else:
                    c.send("False".encode())
                time.sleep(0.1)
                if action != "exit":
                    c.send(answ.encode())
                    time.sleep(0.1)
                else:
                    c.close()
            else:
                c.close()
                break
    except:
        c.close()


while True:
    c, a = soc.accept()
    print("New client from {}:{}".format(a[0], a[1]))
    cThread = threading.Thread(target=one_user, args=(c, a))
    cThread.daemon = True
    cThread.start()
input(".: END :.")

