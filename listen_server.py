import socket
import threading
soc = socket.socket()
soc.bind(("0.0.0.0",9601))
soc.listen(1)
def handler(c, a):
	c.send("01110011 01100101 01100011 01110010 01100101 01110100 01011111 01101101 01100101 01110011 01110011 01100001 01100111 01100101".encode())
	c.close()
while True:
	c, a = soc.accept()
	cThread = threading.Thread(target = handler, args = (c, a))
	cThread.daemon = True
	cThread.start()