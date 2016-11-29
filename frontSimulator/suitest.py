import threading, tkinter as tk
from tkinter import *

import time


class App:
    def __init__(self, root):
        self.root = root
        self.create_frame_bottom()
        self.stopflag = 0

    def create_frame_bottom(self):
        winTs = tk.Frame(self.root, border=4)
        winTs.pack(side='top', anchor='w')
        self.txt0 = tk.Text(winTs, width=160, height=30, border=5, wrap='none')
        self.sly = tk.Scrollbar(winTs, orient=tk.VERTICAL)
        self.sly.config(command=self.txt0.yview)
        self.slx = tk.Scrollbar(winTs, orient=tk.HORIZONTAL)
        self.slx.config(command=self.txt0.xview)
        self.txt0.config(yscrollcommand=self.sly.set, xscrollcommand=self.slx.set)
        # layout
        self.sly.pack(side='right', fill='y', expand=0, anchor=N)
        self.slx.pack(side='bottom', fill='x', expand=0, anchor=N)
        self.txt0.pack(side='left', expand=1, fill='x')

        win0 = tk.Frame(self.root, border=4)
        win0.pack(side='top', anchor='w')

        self.bt1 = tk.Button(win0, text='print', padx=8, command=lambda : self.thr(self.print1))
        self.bt1.pack(side='left')

        self.bt2 = tk.Button(win0, text='stop', padx=8, command=self.stop)
        self.bt2.pack(side='left')

    def stop(self):
        self.stopflag=1

    def thr(self,func):
        t1 = threading.Thread(target=func)
        t1.setDaemon(True)
        t1.start()

    def print1(self):
        for i in range(10):
            if self.stopflag == 1:
                print("stop")
                break
            time.sleep(1)
            print(i)
            self.txt0.insert(1.0, i*200)
            self.txt0.update()
        self.stopflag = 0



root = tk.Tk()
root.title("Thread test")
a = App(root)
root.mainloop()
