from tkinter import *
from tkinter.scrolledtext import ScrolledText
import socket
#import _thread as thread
import threading

fonty = ("Courier",11)
UDP_PORT = 25565

class ChatApp(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.geometry("600x400")

        self.__create_widgets()
        
        self.IP = ""
        self.sock = None

    def __create_socket(self):
        if not self.sock:
            try:
                self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.sock.bind(("localhost",UDP_PORT))
                self.__create_listener()
                self.message("Connected to chat!")
            except Exception:
                self.message("Binding to port failed!")

    def __create_listener(self):
        def receiveData():
            while True:
                data, addr = self.sock.recvfrom(1024)
                self.message(str(data,'utf-8'))
        
        t = threading.Thread(target=receiveData)
        t.setDaemon(True)
        t.start()
            
    
    def __create_widgets(self):
        
        self.chatBox = ScrolledText(self,
                relief=GROOVE,font=fonty,state=DISABLED) #width=80,height=15)
        self.chatBox.place(height=350,width=600)

        self.entry_text = StringVar()
        self.entryBox = Entry(self,width=70,font=fonty,textvariable=self.entry_text)
        self.entryBox.place(width=600,height=25,y=350)
        self.entryBox.bind('<Return>',self.enter)

        self.username = StringVar()
        self.usernameLbl = Label(self, text="Username",font=fonty)
        self.usernameLbl.place(y=375)

        self.userBox = Entry(self,textvariable=self.username,font=fonty)
        self.userBox.place(width=85,height=25,x=80,y=375)

        self.connectLbl = Label(self, text="IP Address",font=fonty)
        self.connectLbl.place(x=170,y=375)

        self.ipAddress = StringVar()
        self.ipBox = Entry(self,textvariable=self.ipAddress)
        self.ipBox.place(width=250,height=25,x=270,y=375)

        self.connectBtn = Button(self, text="Connect",font=fonty,command=self.__create_socket)
        self.connectBtn.place(width=80,height=25,x=520,y=375)
        
    def enter(self, event):
        message = self.entry_text.get().strip()
        if message != "":
            if not self.sock:
                self.message("Error: You aren't connected!")
                return
            
            text = self.username.get() + ": " + self.entry_text.get()

            self.message(text)
            
            self.IP = self.ipAddress.get()
            try:
                print(bytes(text,'utf-8'))
                self.sock.sendto(bytes(text,'utf-8'),(self.IP,UDP_PORT))
            except:
                if self.IP == "":
                    self.message("You need to enter an IP address to send to...")
                else:
                    self.message("Error: message failed to send!")

            print(text)
            self.entryBox.delete(0,len(self.entryBox.get()))
            
    def message(self,text):
        self.chatBox.config(state=NORMAL)
        self.chatBox.insert(INSERT,text + "\n")
        self.chatBox.config(state=DISABLED)

    
            
app = ChatApp()
#app.mainloop()
#root.mainloop()
