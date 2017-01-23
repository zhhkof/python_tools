import psycopg2
import datetime
import random


def randf(min, max, precision=2):
    return round(random.uniform(min, max), precision)


# 风机信息
wfid = 140802
wtid = 140802203
# 数据条数，请自行计算
num = 60 * 24 * 731
# 延续性造数据开关
goon = False
# 数据起始时间，当goon为True且风机存在底量数据时，此项无效
first_time = '2015-01-01 00:00:00'
rectime = datetime.datetime.strptime(first_time, "%Y-%m-%d %H:%M:%S")

conn = psycopg2.connect(database='v5_test', user='postgres', password='postgres', host='10.80.5.43', port='5432')
cur = conn.cursor()

id = [0] * 11
if goon:
    cur.execute('select * from public.onedata where wtid= %s order by rectime desc limit 1', (wtid,))
    row = cur.fetchall()
    if len(row) > 0:
        for i in range(10):
            id[i + 1] = float(row[0][i + 3])
        rectime = row[0][2] + datetime.timedelta(minutes=1)
        id[9] = id[10]
    else:
        rectime = datetime.datetime.strptime(first_time, "%Y-%m-%d %H:%M:%S")
else:
    rectime = datetime.datetime.strptime(first_time, "%Y-%m-%d %H:%M:%S")

for i in range(num):
    id[0] = rectime.strftime("%Y-%m-%d %H:%M:%S")
    id[1] = randf(3, 25)
    id[2] = randf(600, 1100)
    id[3] = randf(800, 1500)
    id[4] = 5
    id[8] = randf(-5, 15)
    id[10] = id[9] + randf(5, 25)
    print(tuple([wfid, wtid] + id))

    cur.execute('''INSERT INTO public.onedata VALUES(%s''' + ',%s' * 12 + ');', tuple([wfid, wtid] + id))
    if i % 50 == 0:
        conn.commit()

    rectime += datetime.timedelta(minutes=1)
    id[9] = id[10]

conn.commit()
conn.close()
