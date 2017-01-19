import psycopg2
import datetime
import random


def randf(min, max, precision=2):
    return round(random.uniform(min, max), precision)


rectime = datetime.datetime.strptime("2016-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

conn = psycopg2.connect(database='2HA', user='postgres', password='postgres', host='10.80.5.43', port='5432')
cur = conn.cursor()

id = [0] * 10
for i in range(120):
    id[0] = randf(3, 25)
    id[1] = randf(600, 1100)
    id[2] = randf(800, 1500)
    id[3] = 5
    id[7] = randf(-5, 15)
    id[9] = id[8]+randf(5, 50)

    id.insert(0, rectime.strftime("%Y-%m-%d %H:%M:%S"))
    print(tuple(id))
    cur.execute('''INSERT INTO public.onedata VALUES(140802, 140802200''' + ',%s' * 11 + ');', tuple(id))
    if i % 50 == 0:
        conn.commit()

    rectime += datetime.timedelta(minutes=1)
    id.pop(0)
    id[8] = id[9]

conn.commit()
conn.close()
