# coding: utf-8
# version 1.1

from tkinter import *
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3


class Application:
    def __init__(self, root):
        self.root = root
        self.create_frame_top()
        self.create_frame_bottom()

    def create_frame_top(self):
        self.frm_top_label = tk.Label(self.root, text="sqlite db数据对比工具")
        self.frm_top_label.grid(row=0, column=0, padx=15, pady=2)

    def create_frame_bottom(self):
        self.frm_bottom = tk.LabelFrame(self.root)
        self.frm_bottom.grid(row=1, column=0, padx=15, pady=2)

        # db1_label
        # self.frm_bottom_label_0 = tk.Label(self.frm_bottom, text="db1路径:")
        # self.frm_bottom_label_0.grid(row=0, column=0, padx=15, pady=2, sticky="e")

        # db1 choose button
        self.frm_bottom_btn_db1 = tk.Button(self.frm_bottom, text="db1测试库文件路径", command=self.open_file1)
        self.frm_bottom_btn_db1.grid(row=0, column=0, padx=15, pady=2, sticky="e")

        # db2_label
        # self.frm_bottom_label_1 = tk.Label(self.frm_bottom, text="db2路径:")
        # self.frm_bottom_label_1.grid(row=1, column=0, padx=15, pady=2, sticky="e")

        # db2 choose button
        self.frm_bottom_btn_db2 = tk.Button(self.frm_bottom, text="db2生产库文件路径", command=self.open_file2)
        self.frm_bottom_btn_db2.grid(row=1, column=0, padx=15, pady=2, sticky="e")

        # tables_label
        self.frm_bottom_label_2 = tk.Label(self.frm_bottom,
                                           text="指定对比的表名:\n(逗号分割,不填则默认所有表)")
        # text="specify tables:\n(e.g. table1,table2\nor blank for all tables)")
        self.frm_bottom_label_2.grid(row=2, column=0, padx=15, pady=2, sticky="e")

        # description
        self.frm_bottom_label_3 = tk.Label(self.frm_bottom,
                                           text="*在对比结果中，只显示db2中\n存在而db1中不存在的数据*", fg="red")
        # text="specify tables:\n(e.g. table1,table2\nor blank for all tables)")
        self.frm_bottom_label_3.grid(row=3, column=0, padx=15, pady=2, sticky="e")

        # db1 path Entry
        self.frm_bottom_entry_var_0_db1 = StringVar()
        self.frm_bottom_entry_0 = tk.Entry(self.frm_bottom, text=self.frm_bottom_entry_var_0_db1)
        self.frm_bottom_entry_0.grid(row=0, column=1, padx=15, pady=2)

        # db2 path Entry
        self.frm_bottom_entry_var_1_db2 = StringVar()
        self.frm_bottom_entry_1 = tk.Entry(self.frm_bottom, text=self.frm_bottom_entry_var_1_db2)
        self.frm_bottom_entry_1.grid(row=1, column=1, padx=15, pady=2)

        # tables Entry
        self.frm_bottom_entry_var_2 = StringVar()
        self.frm_bottom_entry_2 = tk.Entry(self.frm_bottom, text=self.frm_bottom_entry_var_2)
        self.frm_bottom_entry_2.grid(row=2, column=1, padx=15, pady=2)

        # func button
        self.frm_bottom_btn_0 = tk.Button(self.frm_bottom, text="Do compare", command=self.compare)
        self.frm_bottom_btn_0.grid(row=3, column=1, padx=15, pady=2)

    def open_file1(self):
        self.fname_db1 = filedialog.askopenfilename(
            filetypes=(("sqlite files", "*.sqlite;*.db"), ("All files", "*.*")))
        # print(self.fname1)
        self.frm_bottom_entry_var_0_db1.set(self.fname_db1)
        # print(self.frm_bottom_entry_var_0_db1.get())

    def open_file2(self):
        self.fname_db2 = filedialog.askopenfilename(
            filetypes=(("sqlite files", "*.sqlite;*.db"), ("All files", "*.*")))
        # print(self.fname2)
        self.frm_bottom_entry_var_1_db2.set(self.fname_db2)
        # print(self.frm_bottom_entry_var_1_db2.get())

    def compare(self):
        # local_db = "./localdb.sqlite"
        # xw_db = "./localdb_sys.sqlite"
        local_db = str(self.frm_bottom_entry_0.get())
        xw_db = str(self.frm_bottom_entry_1.get())
        tbs_input = str(self.frm_bottom_entry_2.get())

        try:
            conn = sqlite3.connect(local_db)
            c = conn.cursor()
            c.execute("ATTACH DATABASE ? AS db2", (xw_db,))

            # Get tables' names
            diff_tables = []  # 记录db2多的表
            tables_db2 = []  # db2所有表，对应xw_db
            tables_db1 = []  # db1所有表，对应local_db
            exception_list = []  # 记录异常
            # 获取db1所有表记入list
            c.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")
            for tb in c.fetchall():
                tables_db1.append(tb[0])

            if len(tbs_input) == 0:
                # 获取db2所有表记入list
                c.execute("SELECT tbl_name FROM db2.sqlite_master WHERE type='table'")
                for tb in c.fetchall():
                    tables_db2.append(tb[0])
                # 注意：被attach的表，如果含有主表没有的table如tableA,在attach后可直接select * from tableA查出数据。



                # 找出db2中有而db1中没有的表。
                for df_tb in list(set(tables_db2).difference(set(tables_db1))):
                    diff_tables.append(df_tb)

                # print(diff_tables)
                # 用db2的表名来比较。
                tables = tables_db2

            else:
                tables = tbs_input.split(",")
                for tb in tables:
                    # 先只考虑db2表比db1多的情况，db1表多的情况直接抛异常退出。
                    if tb not in tables_db1:
                        diff_tables.append(tb)

            # Compare
            f = open("./Compare_result.txt", 'w+')
            if diff_tables.__len__() > 0:
                f.write("--以下表名只存在db2中,或指定表名分隔符错误: \n" + str(diff_tables) + "\n\n")
            f.write("--共有表差异结果(db2中存在而db1中不存在的数据)：\n")
            for tb in tables:
                # only show the datas in db2 and not in db1.
                try:
                    c.execute('''SELECT * FROM (SELECT * FROM db2.''' + tb + '''
                                EXCEPT
                                SELECT * FROM ''' + tb + ''')''')
                    # UNION ALL
                    # SELECT *,"in local_db" FROM
                    # (SELECT * FROM ''' + table + '''
                    # EXCEPT
                    # SELECT * FROM db2.''' + table + ''')
                    # ''')

                    i = 1  # mark line No.
                    compare_data = c.fetchall()
                    if compare_data.__len__() > 0:
                        f.write("table:" + tb + "\n")
                        for row in compare_data:
                            f.write("   " + str(i) + ": " + str(row) + "\n")
                            i += 1

                            # t = 1  # Just show table name for having difference.when first loop show only.
                            # for row in c.fetchall():
                            #     if row is not None and t == 1:
                            #         f.write("table:" + table + "\n")
                            #         t += 1
                            #     f.write("   " + str(i) + ": " + str(row) + "\n")
                            #     i += 1
                except Exception as e:
                    # 循环中存在异常的加入list，并不跳出，进入下一个循环
                    exception_list.append("\nException (table: " + tb + "): " + str(e) + "\n")
            if len(exception_list) != 0:  # 最终结果里显示所有异常。
                for ex in exception_list:
                    f.write(ex)
                messagebox.showinfo("message", "Done with some Exceptions! See results in Compare_result.txt")
            else:
                messagebox.showinfo("message", "Done! See results in Compare_result.txt")
        except Exception as e:
            f.write("\nException: " + str(e))
            messagebox.showinfo("error", "Error! Log in Compare_result.txt")
        finally:
            f.close()
            c.close()
            conn.close()


# if __name__ == "__main__":
root = tk.Tk()
root.title("sqlite data compare V1.2Beta")
Application(root)
root.mainloop()
