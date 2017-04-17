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
from frontSimulator.xlsxTool import Excel
import threading
from socket import *


# class Application:
#     def __init__(self, root):
#         self.root = root
#         self.frmNoteBook = LabelFrame(self.root, text="功能")
#         self.frmNoteBook.grid(row=0, column=0, sticky='s' + 'w' + 'e' + 'n')
#         note_book = ttk.Notebook(self.frmNoteBook, width=760)
#         self.frmOne = tk.Frame(note_book)
#         note_book.add(self.frmOne, text='1111', padding=3)
#         note_book.grid(row=0, column=0, sticky='s' + 'w' + 'e' + 'n')
#
#
#
#
# root = tk.Tk()
# root.title("工具")
# a = Application(root)
# root.mainloop()

def isServerStart(ip, port):
    s = socket(AF_INET, SOCK_STREAM)
    try:
        if s.connect_ex((ip, port)) == 0:
            return True
        else:
            return False
    except:
        return False

print(isServerStart('10.80.10.248',9999))