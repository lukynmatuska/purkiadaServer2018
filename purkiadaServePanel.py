# -*- coding: utf-8 -*-
import dominate
from dominate.tags import *

class HtmlPage():
    """Class for making an ground of MUI HTML pages"""

    def __init__(self, title, content, filename):
        self.title = "{} - PurkiadaServer".format(title)
        self.menuButtonName = title

        self.menuList = ['Home', 'About', 'Contact', "Login", "Register", "Status"]
        if not self.menuButtonName in self.menuList:
            self.menuList.append(self.menuButtonName)
        self.content =  content
        self.htmlFileName = filename

        self.update()#title, content, filename)
        self.save()
        
    def update(self):#, title, content, filename):
        self.page = dominate.document(title = self.title)

        with self.page.head:
            link(rel='stylesheet', href="http://cdn.muicss.com/mui-0.9.30/css/mui.min.css")#style.css')
            script(type='text/javascript', src="http://cdn.muicss.com/mui-0.9.30/js/mui.min.js")#script.js")

        with self.page.body:
            with div(cls="mui-container"):
                with div(cls="mui-panel"):
                    with div(style="text-align:center"):
                        h1(self.title)
                        for name in self.menuList:
                            if name == "home" or name == "Home":
                                with a(href='./index.html'):
                                    button(name.title(), style="margin-left:auto;margin-right:auto;margin-top:auto;margin-bottom:auto;",cls="mui-btn mui-btn--primary mui-btn--raised")
                            else:
                                with a(href='./%s.html' % name):
                                    button(name.title(), style="margin-left:auto;margin-right:auto;margin-top:auto;margin-bottom:auto;",cls="mui-btn mui-btn--primary mui-btn--raised")
                    hr()
                    if type(self.content) == str:
                        p(self.content)
                    else:
                        div(self.content)
                        
                    with div(cls="paticka", style="text-alig: center;"):
                        hr()
                        with p("Copyright &copy; 2018, ", style="text-align: center; font-size: 75%; border=0%; padding=0%"):
                            a("Buchticka.eu Team", href="http://buchticka.eu")
                            #pass #a("posta@buchticka.eu", href="mailto:posta@buchticka.eu", cls="blind")
            #print(self.page)
            return self.page

    def save(self):#WIP
        #self.htmlFileName = "index" #"mealList"
        self.i = 1
        while True:
            try:
                if self.i == 1:
                    self.f1 = open(".\\panel\{}.html".format(self.htmlFileName), "w")
                    #self.i = ""
                else:
                    self.f1 = open(".\\panel\{}{}.html".format(self.htmlFileName,self.i), "w")
                self.f1.write(str(self.update()))#doc))
                #f1.write(str(week.offerHtml))#doc))
                self.f1.close()
                print("\nFILE NAME: {}{}.html".format(self.htmlFileName, self.i))
                break
            except:
                print("Error with saving html file!")
                self.i += 1

        #self.htmlFileName = "index"
        while True:
            try:
                self.f2 = open("C:\\xampp\\htdocs\\purkiadaServer2018\\{}.html".format(self.htmlFileName), "w")
                self.f2.write(str(self.update()))
                self.f2.close()
                print("FILE NAME: C:\\xampp\\htdocs\\purkiadaServer2018\\{}.html".format(self.htmlFileName))
                break
            except:
                print("Error with saving html file! to C:\\xampp\\htdocs\\purkiadaServer2018\\")
        
        
home = HtmlPage("Home", "Ahoj svete! z Homu", "Home")
status = HtmlPage("Status", "Purkiada Server Panel is working!", "Status")
contact = HtmlPage("Contact", "Ahoj svete! z contact", "Contact")
about = HtmlPage("About", "Ahoj svete! z about", "About")
login = HtmlPage("Login", "Ahoj svete! z login", "Login")
register = HtmlPage("Register", "Ahoj svete! z Register", "Register")
print(".: Websites creation SUCCES COMPLETED! :.")

import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(threadName)-10s] %(message)s',
                    )
def saveIt():
    while True:
        time.sleep(10)
        #home.save()
        status.save()
        #print("Saved at {}".format(time.time()))
        logging.debug("Saved at {}".format(time.asctime( time.localtime(time.time()) )))

def daemon():
    logging.debug('Running')
    saveIt()
    while True:
        #home.update()
        time.sleep(5)
        status.update()
        #print("updated at {}".format(time.time()))
        logging.debug("Updated at {}".format(time.asctime( time.localtime(time.time()) )))

#time.sleep(2)
def deamonStop():
    logging.debug('Exiting')

d = threading.Thread(name='daemon', target=daemon)
d.setDaemon(True)

def non_daemon():
    logging.debug('Starting')
    logging.debug('Exiting')

#t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
#t.start()

d.join(1)
#print 'd(isAlive()', d.isAlive())
#t.join()    
#print("Stoppped")
