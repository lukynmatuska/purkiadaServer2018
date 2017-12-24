import socket

actions = ["ls","ssh","help","listen","exit","cd", "rm *","disconect", "cd.."]
def showHelp():
    print("for this help write: help")
    print("for connection with target server write: ssh [adress]:[port]")
    print("if you want to listen data coming from port write: listen [adress]:[port]")
    print("if you want to show files or directories write: dir")
    print("if you want to go do target direstory write: cd [target_directory]")
    print("if you want to remove all files in directory write: rm *")
    print("if you want to disconect the server write: disconect")
    print("if you want to leave write: exit")
showHelp()
connect = False
print("now let's start write action")
conected=""
path = ""
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    action = input(conected+path+"~$ ")
    action = action.split(" ")

    if  connect != True and action[0] != "listen":
        if action[0] == "ssh":
            try:
                adr, port = action[1].split(":")
                soc.connect((adr,int(port)))
                connect = True
                print("new connection with "+adr+" on port: "+str(port))
                connected=adr
                path=soc.recv(1024).decode("utf8")
            except:
                print("wrong adress or port")
        if action[0] == "listen":
            try:
                adr, port = action[1].split(":")
                soc.connect((adr,int(port)))
                print("server found, listening on port:"+str(port)+"\n")
                b_data=soc.recv(2048).decode("utf8")
            except:
                print("host not found")
    if action[0] == "help":
        showHelp()
    if action[0] == "exit":
        exit()
    if action[0] == "disconect" and connect == True:
        conected = ""
        path = ""
        connect=False
    if action[0] not in actions:
        print("unknown command")
    if action[0] not in actions and connect == True:
        soc.send("I_dont_know".encode())
    if connect:
        if action[0] == "ls":
            soc.send("ls".encode())
            data=soc.recv(1024).decode("utf8")
            data = data.split(" ")
            for i in data:
                if i != " ":
                    print(i)
        if action[0] == "cd":
            soc.send((action[0]+" "+action[1]).encode())
            path=soc.recv(1024).decode("utf8")

        """if action[0] == "cd..":
            soc.send("cd..".encode())
            path=soc.recv(1024).decode("utf8")
            """
        if action[0] == "rm *" and path == "/home/root/logs/":
            soc.send("rm *".encode())
            print(soc.recv(1024).decode("utf8"))

