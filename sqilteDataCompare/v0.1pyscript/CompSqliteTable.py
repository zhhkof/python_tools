# -*-coding = utf-8-*-

import sqlite3
import os

# Connect to sqlite and attatch database
# conn = sqlite3.connect(os.path.join("data", "db", "D:\XXXXX\localdb.sqlite"))
local_db = "./localdb.sqlite"
xw_db = "./localdb_sys.sqlite"

conn = sqlite3.connect(local_db)
c = conn.cursor()
c.execute("ATTACH DATABASE ? AS db2", (xw_db,))
# Get all tables' names
c.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")

# Compare
f = open("./Compare_result.txt", 'w+')
tables = c.fetchall()
for tb in tables:
    table = tb[0]
    c.execute('''SELECT *,"in xw_db" FROM (SELECT * FROM db2.''' + table + '''
                    EXCEPT
                    SELECT * FROM ''' + table + ''')
                    UNION ALL
                    SELECT *,"in local_db" FROM
                    (SELECT * FROM ''' + table + '''
                    EXCEPT
                    SELECT * FROM db2.''' + table + ''')''')

    i = 1  # mark line No.

    compare_data = c.fetchall()
    if compare_data.__len__() > 0:
        f.write("table:" + table + "\n")
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

f.close()
c.close()
conn.close()
