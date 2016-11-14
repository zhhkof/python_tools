a = [(1,), (2,), (3,), (4,), (5,)]
b = [(2,), (4,), (6,)]
print((set(a).difference(set(b))))
a=[(1,2),(3,4),(5,6)]
b=[(3,4),(2,1)]

print(list(set([(1,2),(3,4)]).difference(set([(1,2),(3,5)]))))
print((set(a).intersection(set(b))))


# c.execute("PRAGMA TABLE_INFO(propaths)")
# res = c.fetchall()
# tablesstruct = {}
# for r in res:
#     tablesstruct[r[1]] = r[2]
# print(tablesstruct)
w=[1,2,3,4,5,6,7]
m=[1,2]
print(set(w)-set(m))
for i in iter(w):
    if i== 3:
        w.remove(i)
    print(i)
print(w)
