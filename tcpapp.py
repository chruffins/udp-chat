from tkinter import *
from tkinter.scrolledtext import ScrolledText
import socket
#import _thread as thread
import threading

fonty = ("Courier",11)
TCP_PORT = 25565

class ChatApp(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.geometry("600x400")
        self.title("Chat App")

        self.__create_widgets()

        self.IP = ""
        self.listener = None
        self.sender = None
        self.bound = False
        
    def receiveData(self):
        self.conn, addr = self.listener.accept()
        self.message("Connected to {0}!".format(addr))
        while self.bound:
            try:
                data = self.conn.recv(1024)
                self.message(str(data,'utf-8'))
            except Exception:
                pass

    def __create_socket(self):
        def v4or6():
            ip = self.ipAddress.get()
            return 6 and len(ip) > 15 or 4
                
        if self.listener != None:
            self.listener.close()
            self.sender.close()
        try:
            if v4or6() == 4:
                self.listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.sender = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            else:
                self.listener = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
                self.sender = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)

            self.bound = True
            self.__create_listener()
            self.message("Connecting to {0}...".format(self.ipAddress.get()))
            self.sender.connect((self.ipAddress.get(), TCP_PORT))
            
            
        except Exception as e:
            self.message("Connection failed! " + repr(e))
                

    def __create_listener(self):
        try:
            self.listener.bind(("",TCP_PORT))
            self.listener.listen()
            self.bound = True
            if self.bound:
                self.thread = threading.Thread(target=self.receiveData)
                self.thread.setDaemon(True)
                self.thread.start()
                #self.message("Connected to chat!")
        except:
            self.message("Failed to create chat listener!")
            
    
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
            if not self.sender:
                self.message("Error: You aren't connected!")
                return
            
            text = self.username.get() + ": " + self.entry_text.get()

            self.message(text)
            
            try:
                #print(bytes(text,'utf-8'))
                self.sender.send(bytes(text,'utf-8'))
            except:
                self.message("Error: message failed to send!")

            print(text)
            self.entryBox.delete(0,len(self.entryBox.get()))
            
    def message(self,text):
        self.chatBox.config(state=NORMAL)
        self.chatBox.insert(INSERT,text + "\n")
        self.chatBox.config(state=DISABLED)

    
            
app = ChatApp()
app.mainloop()
#root.mainloop()
