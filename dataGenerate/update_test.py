import psycopg2
import datetime
import random


def randf(min, max, precision=2):
    return round(random.uniform(min, max), precision)


wfid = 140802
wtids = [140802200, 140802201, 140802202, 140802203]
num = 1
start_time_str = "2016-07-01 00:00:00"
end_time_str = "2016-08-01 00:00:00"

conn = psycopg2.connect(database='v5_test', user='postgres', password='postgres', host='10.80.5.58', port='5432')
cur = conn.cursor()

st = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
et = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

while st < et:
    ste = st + datetime.timedelta(days=1)
    sql = '''update public.onedata set wtstatus = '2',limitstatus='0',faultcode='0',stopcode='2',limitcode='0'  where wtstatus = '5' and wtid in (140802200, 140802201, 140802202, 140802203) and ((onedata.endelec - onedata.beginelec) - onedata.theorypower / 60) < 0 and (rectime between ''' + st.strftime(
        "'%Y-%m-%d %H:%M:%S'") + ''' and ''' + ste.strftime("'%Y-%m-%d %H:%M:%S'") + ')'
    print(str(num) + ' : ' + sql)
    cur.execute(sql)
    conn.commit()
    st = ste
    num += 1

conn.commit()
conn.close()
