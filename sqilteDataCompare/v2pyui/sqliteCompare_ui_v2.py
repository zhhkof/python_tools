from sqilteDataCompare.v2pyui.sqlitedb import SqliteDB
# cs_db = sqlitedb.SqliteDB('''C:\\Users\\itlocal\\Desktop\\localdb_xw.sqlite''')
# print(cs_db.get_allTableNames())
# print(cs_db.get_tableStruct("propaths"))
# cs_db.close()

# coding: utf-8
# version 1.1

from tkinter import *
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox


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

        # db1 path Entry
        self.text_db1path = StringVar()
        self.entry_db1 = tk.Entry(self.frm_bottom, textvariable=self.text_db1path)
        self.entry_db1.grid(row=0, column=1, padx=15, pady=2)

        # db2 path Entry
        self.text_db2path = StringVar()
        self.entry_db2 = tk.Entry(self.frm_bottom, textvariable=self.text_db2path)
        self.entry_db2.grid(row=1, column=1, padx=15, pady=2)

        # tables Entry
        self.entry_tablesinput = tk.Entry(self.frm_bottom)
        self.entry_tablesinput.grid(row=2, column=1, padx=15, pady=2)

        # db1 choose button
        self.frm_bottom_btn_db1 = tk.Button(self.frm_bottom, text="db1测试库文件路径",
                                            command=lambda: open_file(self.text_db1path))
        self.frm_bottom_btn_db1.grid(row=0, column=0, padx=15, pady=2, sticky="e")

        # db2 choose button
        self.frm_bottom_btn_db2 = tk.Button(self.frm_bottom, text="db2生产库文件路径",
                                            command=lambda: open_file(self.text_db2path))
        self.frm_bottom_btn_db2.grid(row=1, column=0, padx=15, pady=2, sticky="e")

        # tables_label
        self.frm_bottom_label_2 = tk.Label(self.frm_bottom,
                                           text="指定对比的表名:\n(逗号分割,不填则默认所有表)")
        self.frm_bottom_label_2.grid(row=2, column=0, padx=15, pady=2, sticky="e")

        # description
        self.frm_bottom_label_3 = tk.Label(self.frm_bottom,
                                           text="*在对比结果中，只显示db2中\n存在而db1中不存在的数据*", fg="red")
        self.frm_bottom_label_3.grid(row=3, column=0, padx=15, pady=2, sticky="e")

        # func button
        self.frm_bottom_btn_0 = tk.Button(self.frm_bottom, text="Do compare",
                                          command=lambda: compare(self.entry_db1.get(), self.entry_db2.get(),
                                                                  self.entry_tablesinput.get()))
        self.frm_bottom_btn_0.grid(row=3, column=1, padx=15, pady=2)


def compare(local_db, xw_db, tbs_input=''):
    # local_db = self.entry_db1.get()
    # xw_db = self.entry_db2.get()
    # tbs_input = self.entry_tablesinput.get()
    f = open("./Compare_result.txt", 'w+')

    db1 = SqliteDB(local_db)
    connresult1 = db1.do_connect()
    db2 = SqliteDB(xw_db)
    connresult2 = db2.do_connect()
    # 对数据库连接和attache database做异常获取
    if (connresult1, connresult2) != (1, 1):
        messagebox.showinfo("ERROR", "Error! Log in Compare_result.txt")
        f.write("Exception: db connect error!")
        f.close()
        return 0
    diff_tables2 = []  # 记录db2多的差异表
    diff_tables1 = []  # 记录db1多的差异表
    exception_list = []  # 记录异常
    diff_structs = []  # 记录表结构差异[(table,[(key,value)])]
    # 获取db1所有表记入list
    tables_db1 = db1.get_allTableNames()
    # 获取db2所有表记入list
    tables_db2 = db2.get_allTableNames()
    # 两库表的交集。
    intersection_tables = list(set(tables_db2).intersection(set(tables_db1)))

    # 先只考虑db2表比db1多的情况，db1表多的情况不考虑。
    if len(tbs_input) == 0:
        # 以db2的表名遍历比较。
        tables = intersection_tables
        # 找出db2中有而db1中没有的表。
        for df_tb in list(set(tables_db2).difference(set(tables_db1))):
            diff_tables2.append(df_tb)
        for df_tb in list(set(tables_db1).difference(set(tables_db2))):
            diff_tables1.append(df_tb)


    else:
        # 解析输入的表来比较
        tables = tbs_input.split(",")
        for tb in tables:
            # 同上if
            if tb not in tables_db1 and tb in tables_db2:
                diff_tables2.append(tb)
            elif tb not in tables_db2 and tb in tables_db1:
                diff_tables1.append(tb)
        tables = list(set(tables)-(set(diff_tables1).union(set(diff_tables2))))

    # 结果列出表差异
    if len(diff_tables1) > 0:
        f.write("--以下表只存在db1测试库中: \n" + str(diff_tables1) + "\n\n")
    if len(diff_tables2) > 0:
        f.write("--以下表只存在db2生产库中: \n" + str(diff_tables2) + "\n\n")


    # 比较输入表的结构，只列出db2中多的或与db1字段类型不一致的。
    diff_structtable=[]
    for tb in tables:
        dfs2 = list(set(db2.get_tableStruct(tb)).difference(set(db1.get_tableStruct(tb))))
        dfs1 = list(set(db1.get_tableStruct(tb)).difference(set(db2.get_tableStruct(tb))))
        if len(dfs2) > 0 or len(dfs1) > 0:
            diff_structs.append((tb, dfs1, dfs2))
            diff_structtable.append(tb)
    tables = list(set(tables) - set(diff_structtable))
    if len(diff_structs) > 0:
        f.write("--以下表字段有不一致，将不做数据对比:\n")
        for s in diff_structs:
            f.write("table: " + str(s[0]) + '\n')
            f.write("测试库: " + str(s[1]) + '\n')
            f.write("生产库: " + str(s[2]) + '\n')
            f.write("------------------------\n")

    # Compare
    try:
        db1.attach_database(db2.get_dbPath(), "db2")
    except Exception as e:
        messagebox.showinfo("ERROR", "attach database error!")
        f.write("Error: " + str(e))
        f.close()
        return 0
    f.write("\n--共有表差异结果(db2生产库中存在而db1测试库不存在的数据)：\n")
    for tb in tables:
        # 根据要求，只查出db2中有而db1中没有的数据。
        sql = '''SELECT * FROM (SELECT * FROM db2.''' + tb + '''
                            EXCEPT
                            SELECT * FROM ''' + tb + ''')'''
        i = 1  # mark line No.
        try:
            compare_data = db1.get_excResult(sql)
            if len(compare_data) > 0:
                f.write("table:" + tb + "\n")
                for row in compare_data:
                    f.write("   " + str(i) + ": " + str(row) + "\n")
                    i += 1
        except Exception as e:
            # 循环中存在异常的加入list，并不跳出，进入下一个循环
            exception_list.append("\nException (table: " + tb + "): " + str(e) + "\n")
    f.write("\n---以上为全部对比结果---\n\n")
    if len(exception_list) != 0:  # 最终结果里显示所有异常。
        f.write("\n***对比过程中出现的异常***")
        for ex in exception_list:
            f.write(ex)
        messagebox.showinfo("message", "Done with some Exceptions! See results in Compare_result.txt")
    else:
        messagebox.showinfo("message", "Done! See results in Compare_result.txt")
    f.close()
    db1.close()
    db2.close()


def open_file(entry_text):
    fname = filedialog.askopenfilename(
        filetypes=(("sqlite files", "*.sqlite;*.db"), ("All files", "*.*")))
    entry_text.set(fname)


# if __name__ == "__main__":
root = tk.Tk()
root.title("sqlite data compare V2.0Beta")
Application(root)
root.mainloop()
