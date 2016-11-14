from tkinter import *
import tkinter.messagebox as messagebox
import os

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.db1label= Label(self, text="db1:")
        self.db1label.pack()
        self.db1path = Entry(self)
        self.db1path.pack()
        self.button = Button(self, text="Do compare", command=self.hello)
        self.button.pack()
        self.db2label= Label(self, text="db2:")
        self.db2label.pack()
        self.db2path = Entry(self)
        self.db2path.pack()


    def hello(self):
        db = self.db1path.get()
        messagebox.showinfo("message", "db is %s" % db)

app=Application()
app.master.title("test")
app.mainloop()