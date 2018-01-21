# -*- coding: utf-8 -*-
import sys
import socket
import threading
import time
import logging

import loadTable
import purkiadaServerPanel

#import dominate as dominate
#from dominate.tags import *

path = "home/"  # "default" ukazatel kde jsem v jaké složce
while True:
    try:
        users_file = open("users.txt", "r+")
        user_names = users_file.readlines()
        users_file.close()
        print("From users.txt: {}".format(user_names))
        break
    except:
        users_file = open("users.txt", "w")
        users_file.write("admin-admin\n")
        users_file.write("user-1234")
        users_file.close()


#print("{}".format(loadTable.users))
connectedUsers = []
connectedUsersNames = []

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
        self.admin_pass = "secret_message"
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
            self.acess = True
            try:
                self.pathList = self.pathList[0]
            except:
                pass
        else:
            isthere = False
            for i in self.directory.content:
                if i.name == self.argv:
                    isthere == True
            if isthere == False:
                self.acess = True
            for dir in self.directory.content:
                if dir.name == self.argv:
                    print("soubor je tady")
                    print(self.perrmission)
                    print("\n")
                    print(dir.acess)
                    if self.perrmission in dir.acess:
                        print("práva souhlasí")
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

loadTable.users.append("admin")
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
    soc.bind(("0.0.0.0", 9600))
name = soc.getsockname()
logging.debug("Server started on {}:{}".format(name[0], name[1]))
#print(name)
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
    #try:
    user = User(path, home, a)

    c.send(banner.encode())
    time.sleep(0.2)
    c.send(path.encode())

    #část kodu, která se změní
    #while user.connected == False:
    while not user.connected:
        #print("WHILE")
        data = c.recv(1024).decode("utf8")
        user.name = data.split("-")[0]
        user.pswd = data.split("-")[1]
        for username in loadTable.users:#user_names:
            tmpPswd = loadTable.users.index(username)
            #print("{}:{}--{}:{}".format(user.name, user.pswd, user.name == username, tmpPswd == user.pswd))
            #print("{}:{}".format(username, loadTable.pswds[tmpPswd]))
            if user.name == username and loadTable.pswds[tmpPswd] == user.pswd:
                c.send("True".encode())
                user.connected = True
                #here we must add user to connected users (list)
                connectedUsers.append(user)
                connectedUsersNames.append(user.name)
                print(connectedUsersNames)
            """for username in loadTable.users:
                if data in username:
                    c.send("True".encode())
                    user.connected = True
                    #here we must add user to connected users (list)
                    connectedUsers.append(user)
                    print(connectedUsers)"""
            #if user.connected == False:
        if not user.connected:
            c.send("False".encode())

        
                
    while True:
        action = c.recv(1024).decode("utf8")
        print("action: \"{}\"".format(action))
        #userLog = open("/home/hojang/Users_Logs/"+user.name + "_Log.txt", "a")
        userLog = open("C:\\Users\\buchmaier.jan\\Desktop\\User_Log\\{}_Log.txt".format(user.name), "a")
        #userLog.write(action+"\n")
        userLog.write("[{}] {}\n".format(time.time(), action))
        userLog.close()
        if action != "disconnect":
            user.acess = False
            user.answerToClient = "None"
            answ = user.run(action)
            print(user.acess)
                #if user.acess == True:
            if user.acess:
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
    #except:
        #c.close()

def htmlUsers():
    purkiadaServerPanel.status.add(purkiadaServerPanel.h3("Active users:"))
    #purkiadaServerPanel.status.content += purkiadaServerPanel.h3("Active users:")
    purkiadaServerPanel.status.add(purkiadaServerPanel.p(connectedUsersNames))
    #purkiadaServerPanel.status.content += purkiadaServerPanel.p(connectedUsers)
    purkiadaServerPanel.logging.debug("Successfully started!")

a = threading.Thread(name="Server panel", target=htmlUsers)
a.setDaemon(True)
#htmlUsers()

while True:
    c, a = soc.accept()
    print("New client from {}:{}".format(a[0], a[1]))
    cThread = threading.Thread(target=one_user, args=(c, a))
    cThread.daemon = True
    cThread.start()
input(".: END :.")

