import sqlite3

class SqliteDB:
    def __init__(self, db_path):
        self.db_path = db_path

    def do_connect(self):
        if len(self.db_path) > 0:
            self.conn = sqlite3.connect(self.db_path)
            self.cur = self.conn.cursor()
            return 1
        else:
            return 0

    def attach_database(self, db2_path, alias="db2"):
        self.cur.execute("ATTACH DATABASE ? AS " + alias, (db2_path,))

    def get_allTableNames(self):  # 获取db所有表名，放入list
        tableNames = []
        self.cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")
        for tb in self.cur.fetchall():
            tableNames.append(tb[0])
        return tableNames

    def get_tableStruct(self, tableName):  # 获取单个表结构，返回dict
        self.cur.execute("PRAGMA TABLE_INFO(%s)" % tableName)
        res = self.cur.fetchall()
        # 只取字段名称和类型
        tableStruct = []
        for r in res:  # 只取两列，key列字段名，value字段类型，忽略大小写。
            tableStruct.append((r[1].lower(), r[2].lower()))
        return tableStruct

    def get_dbPath(self):
        return self.db_path

    def get_excResult(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
