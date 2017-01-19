import psycopg2
import datetime
import random


def randf(min, max, precision=2):
    return round(random.uniform(min, max), precision)

wfid=140802
wtid=140802200
rectime = datetime.datetime.strptime("2016-07-01 00:00:00", "%Y-%m-%d %H:%M:%S")

conn = psycopg2.connect(database='2HA', user='postgres', password='postgres', host='10.80.5.43', port='5432')
cur = conn.cursor()

id = [0] * 11
for i in range(120):
    id[0] = rectime.strftime("%Y-%m-%d %H:%M:%S")
    id[1] = randf(3, 25)
    id[2] = randf(600, 1100)
    id[3] = randf(800, 1500)
    id[4] = 5
    id[8] = randf(-5, 15)
    id[10] = id[9]+randf(5, 50)
    print(tuple([wfid,wtid]+id))

    cur.execute('''INSERT INTO public.onedata VALUES(%s''' + ',%s' * 12 + ');', tuple([wfid,wtid]+id))
    if i % 50 == 0:
        conn.commit()

    rectime += datetime.timedelta(minutes=1)
    id[9] = id[10]

conn.commit()
conn.close()
