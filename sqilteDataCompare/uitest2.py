# -*-coding = utf-8-*-

import tkinter as tk
from tkinter import filedialog,StringVar


class Application:
    def __init__(self, root):
        self.root = root
        self.create_frame_top()

    def create_frame_top(self):

        self.frm_bottom = tk.LabelFrame(self.root)
        self.frm_bottom.grid(row=1, column=0, padx=15, pady=2)

        self.frm_top_label = tk.Label(self.root, text="sqlite db数据对比工具")
        self.frm_top_label.grid(row=0, column=0, padx=15, pady=2)

        self.frm_bottom_entry_var_0_db1 = StringVar()
        self.frm_bottom_entry_0 = tk.Entry(self.frm_bottom, text=self.frm_bottom_entry_var_0_db1)
        self.frm_bottom_entry_0.grid(row=0, column=1, padx=15, pady=2)


        self.frm_bottom_btn_0 = tk.Button(self.frm_bottom, text="Do compare", command=self.open_file1)
        self.frm_bottom_btn_0.grid(row=0, column=2, padx=15, pady=2)

        self.frm_bottom_entry_var_1_db2 = StringVar()
        self.frm_bottom_entry_1 = tk.Entry(self.frm_bottom, text=self.frm_bottom_entry_var_1_db2)
        self.frm_bottom_entry_1.grid(row=1, column=1, padx=15, pady=2)

        self.frm_bottom_btn_1 = tk.Button(self.frm_bottom, text="Do compare", command=self.open_file2)
        self.frm_bottom_btn_1.grid(row=1, column=2, padx=15, pady=2)

    def open_file1(self):
        self.fname1 = filedialog.askopenfilename(
            filetypes=(("sqlite files", "*.sqlite;*.db"), ("All files", "*.*")))
        print(self.fname1)
        self.frm_bottom_entry_var_0_db1.set(self.fname1)
        print(self.frm_bottom_entry_var_0_db1.get())
    def open_file2(self):
        self.fname2 = filedialog.askopenfilename(
            filetypes=(("sqlite files", "*.sqlite;*.db"), ("All files", "*.*")))
        print(self.fname2)
        self.frm_bottom_entry_var_1_db2.set(self.fname2)
        print(self.frm_bottom_entry_var_1_db2.get())

root = tk.Tk()
Application(root)
root.mainloop()


# a = "123"
# print(a.split(","))


