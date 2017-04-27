# coding: utf-8
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox
import time
import hashlib
from frontSimulator.socketTool import *
from frontSimulator.FrontTcpServer import *
from frontSimulator.xlsxTool import Excel
from socket import *


class Application:
    def __init__(self, root):
        self.root = root
        self.frmNoteBook = LabelFrame(self.root, text="功能")
        self.frmNoteBook.grid(row=0, column=0, sticky='s' + 'w' + 'e' + 'n')
        note_book = ttk.Notebook(self.frmNoteBook, width=760)
        self.frmOne = tk.Frame(note_book)
        note_book.add(self.frmOne, text='1111', padding=3)
        note_book.grid(row=0, column=0, sticky='s' + 'w' + 'e' + 'n')
        self.create_tcp_server_for_gw750(self.frmOne)

    def create_tcp_server_for_gw750(self, root_fr):
        server_frame = tk.Frame(root_fr, border=4)
        server_frame.pack(side='top', anchor='w')

        server_ip = tk.StringVar(root_fr, '0.0.0.0')
        tk.Label(server_frame, text='  服务ip： ').pack(side='left')
        ttk.Combobox(server_frame, textvariable=server_ip, values=get_ipList(), width='14').pack(side='left')

        port = tk.IntVar(root_fr, 8801)
        tk.Label(server_frame, text='  端口： ').pack(side='left')
        # ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(server_frame, width='6', textvariable=port).pack(side='left')
        # button_start_server = tk.Button(server_frame, text='start', padx=8,
        #                                 command=lambda: TcpServer750(server_ip.get(), port.get()).start())
        button_start_server = tk.Button(server_frame, text='start', padx=8,
                                        command=lambda :self.do_with_thread(TcpServer750('10.80.10.248', 9999).run))
        button_start_server.pack(side='left')


    def do_with_thread(self,func):
        t1 = threading.Thread(target=func)
        t1.setDaemon(True)
        t1.start()


root = tk.Tk()
root.title("工具")
a = Application(root)
root.mainloop()

# def isServerStart(ip, port):
#     s = socket(AF_INET, SOCK_STREAM)
#     try:
#         if s.connect_ex((ip, port)) == 0:
#             return True
#         else:
#             return False
#     except:
#         return False
#
#
# def get_ipList():
#     try:
#         iplist = gethostbyname_ex(gethostname())[2]
#         iplist.reverse()
#         return iplist
#     except Exception as e:
#         print(e)
#         return []