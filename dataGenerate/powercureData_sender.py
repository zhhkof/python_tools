from frontSimulator.socketTool import *
import time
import random, datetime


def randf(min, max, precision=2):
    return round(random.uniform(min, max), precision)


wtids = [140802200, 140802201, 140802202, 140802203]


for wtid in wtids:
    start_time_str = "2016-12-01 00:00:00"
    end_time_str = "2017-01-01 00:00:00"
    st = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    et = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
    while st < et:
        send_data = '''(sediment|@time|(powercurve|@wtid|@wspeed,@power,25.54))'''
        send_data = send_data.replace('@time', st.strftime("%Y-%m-%d %H:%M:%S"))
        send_data = send_data.replace('@wtid', str(wtid))
        sp=randf(2, 13)
        send_data = send_data.replace('@wspeed', str(sp))
        send_data = send_data.replace('@power', str(round(sp*random.uniform(100, 150),2)))
        print(tcp_send('10.80.5.54', 8804, send_data))
        # print(send_data)
        st += datetime.timedelta(hours=random.randint(6,20))
