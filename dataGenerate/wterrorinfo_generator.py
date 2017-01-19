import hashlib

import psycopg2
import datetime
import random


def randf(min, max, precision=2):
    return round(random.uniform(min, max), precision)


def generate_unique_code(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    l = list(m.hexdigest())
    l[7] += '-'
    l[11] += '-'
    l[15] += '-'
    l[19] += '-'
    return ''.join(l)


wfid = 140802
wtid = 140802200
rectime = datetime.datetime.strptime("2016-01-01 08:00:00", "%Y-%m-%d %H:%M:%S")

conn = psycopg2.connect(database='2HA', user='postgres', password='postgres', host='10.80.5.43', port='5432')
cur = conn.cursor()

id = [0] * 7
for i in range(10):
    # 故障
    id[0] = rectime.strftime("%Y-%m-%d %H:%M:%S")
    id[1] = random.choice([133, 106, 107, 122, 174])
    id[2] = None
    id[3] = None
    id[4] = 1
    id[5] = generate_unique_code(str(wfid) + str(wtid) + str(id[1]) + rectime.strftime("%Y-%m-%d %H:%M:%S"))
    id[6] = 0
    print(i + 1, ':', tuple([wfid, wtid] + id))
    cur.execute('''INSERT INTO public.wterrorinfo VALUES(%s''' + ',%s' * 8 + ');', tuple([wfid,wtid]+id))

    # 销缺
    id[0] = (rectime + datetime.timedelta(hours=random.randint(4, 10))).strftime("%Y-%m-%d %H:%M:%S")
    id[1] = 0
    id[2] = None
    id[3] = None
    id[4] = 2
    id[5] = generate_unique_code(str(wfid) + str(wtid) + str(id[1]) + rectime.strftime("%Y-%m-%d %H:%M:%S"))
    id[6] = 0
    print(tuple([wfid, wtid] + id))
    cur.execute('''INSERT INTO public.wterrorinfo VALUES(%s''' + ',%s' * 8 + ');', tuple([wfid,wtid]+id))
    if i % 50 == 0:
        conn.commit()

    rectime += datetime.timedelta(days=1)

conn.commit()
conn.close()
