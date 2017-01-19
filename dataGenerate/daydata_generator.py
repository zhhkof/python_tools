import psycopg2
import datetime
import random


def randf(min, max, precision=2):
    return round(random.uniform(min, max), precision)


rectime = datetime.datetime.strptime("2016-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

conn = psycopg2.connect(database='2HA', user='postgres', password='postgres', host='10.80.5.43', port='5432')
cur = conn.cursor()

id = [0] * 125
for i in range(366):
    id[0] = randf(7, 18)
    id[1] = randf(0, 3)
    id[2] = randf(18, 35)
    id[3] = randf(1000, 1800)
    id[4] = randf(800, 1000)
    id[5] = randf(1500, 1800)
    id[6] = randf(0, 1385)
    id[7] = randf(-400, 0)
    id[8] = randf(5, 1800)
    id[9] = randf(123, 345)
    id[10] = randf(123, 345)
    id[11] = randf(123, 345)
    id[12] = randf(123, 345)
    id[13] = randf(123, 345)
    id[14] = randf(123, 345)
    id[15] = randf(40, 1000)
    id[16] = randf(-200, 20)
    id[17] = randf(800, 1800)

    id[19] = id[18] + randf(5000, 10000)
    id[21] = id[20] + randf(3, 4)
    id[23] = id[22] + randf(20, 24)
    id[25] = id[24] + randf(2, 4)
    id[27] = id[26] + randf(20, 24)
    id[29] = id[28] + randf(20, 24)
    id[31] = id[30] + randf(0, 10)
    id[33] = id[32] + randf(0, 10)
    id[35] = id[34] + randf(0, 10)

    id[36] = randf(1.27, 185.62)
    id[37] = randf(-0.03, 16.57)
    id[38] = randf(3.54, 99.9)
    id[39] = randf(-0.23, 1386.74)
    id[40] = randf(-400, 0)
    id[41] = randf(-0.28, 1800)
    id[42] = randf(0.14, 185.62)
    id[43] = randf(6.9, 99.9)
    id[44] = randf(-0.2, 40.29)
    id[45] = randf(0, 26.79)
    id[46] = randf(0, 67.25)
    id[47] = randf(0, 78.4)
    id[48] = randf(0, 72.97)
    id[49] = randf(0, 87.59)
    id[50] = randf(0, 57.65)
    id[51] = randf(0, 67.8)
    id[52] = randf(0, 22.06)
    id[53] = randf(0, 25.7)
    id[54] = randf(0, 20.31)
    id[55] = randf(0, 28)
    id[56] = randf(-1.63, 1385.8)
    id[57] = randf(-1.64, 1386.02)
    id[58] = randf(-1.74, 1385.89)
    id[59] = randf(6.07, 1385.89)
    id[60] = randf(6.25, 1385.95)
    id[61] = randf(6.14, 1385.89)
    id[62] = randf(4.22, 1385.89)
    id[63] = randf(3.62, 1385.89)
    id[64] = randf(4.25, 1385.89)
    id[65] = randf(2.7, 1385.89)
    id[66] = randf(2.93, 1385.89)
    id[67] = randf(2.82, 1385.89)
    id[68] = randf(4.3, 1800)
    id[69] = randf(4.22, 1385.89)
    id[70] = randf(4.5, 1800)
    id[71] = randf(3.62, 1385.98)
    id[72] = randf(0, 99.9)
    id[73] = randf(-504.89, 477.04)
    id[74] = randf(7.81, 99.9)
    id[75] = randf(-4.8, 1800)
    id[76] = randf(-2, 1800)
    id[77] = randf(-2, 1800)
    id[78] = randf(-1.79, 1800)
    id[79] = randf(6.5, 1800)
    id[80] = randf(6.8, 1800)
    id[81] = randf(6.8, 1800)
    id[82] = randf(4.3, 1800)
    id[83] = randf(4.5, 1800)
    id[84] = randf(4.5, 1800)
    id[85] = randf(3.29, 1800)
    id[86] = randf(3.4, 1800)
    id[87] = randf(3.9, 1800)
    id[88] = randf(2.09, 1800)
    id[89] = randf(6.09, 1800)
    id[90] = randf(0, 123123)
    id[91] = randf(0, 39.92)
    id[92] = randf(0, 48.17)
    id[93] = randf(0, 28.05)
    id[94] = randf(0, 28.2)
    id[95] = randf(0, 42.29)
    id[96] = randf(0, 52.12)
    id[97] = randf(0, 41.45)
    id[98] = randf(0, 50.42)
    id[99] = randf(0, 27.46)
    id[100] = randf(0, 33.09)
    id[101] = randf(0, 21.64)
    id[102] = randf(0, 25)

    id[104] = id[103] + randf(15, 20)
    id[106] = id[105] + randf(15, 20)
    id[108] = id[107] + randf(15, 20)
    id[110] = id[109] + randf(15, 20)
    id[112] = id[111] + randf(15, 20)
    id[114] = id[113] + randf(15, 20)
    id[116] = id[115] + randf(15, 20)
    id[118] = id[117] + randf(15, 20)

    id[119] = randf(24.58, 1414.36)
    id[120] = randf(0, 1161.2)
    id[121] = randf(8.57, 1584.58)
    id[122] = 0
    id[123] = 0
    id[124] = randf(10.58, 348.11)
    id.insert(0, rectime.strftime("%Y-%m-%d %H:%M:%S"))
    print(tuple(id))
    cur.execute('''INSERT INTO public.daydata VALUES(140802, 140802200''' + ',%s' * 126 + ');', tuple(id))
    if i % 50 == 0:
        conn.commit()

    rectime += datetime.timedelta(days=1)
    id.pop(0)
    id[18] = id[19]
    id[20] = id[21]
    id[22] = id[23]
    id[24] = id[25]
    id[26] = id[27]
    id[28] = id[29]
    id[30] = id[31]
    id[32] = id[33]
    id[34] = id[35]
    id[103] = id[104]
    id[105] = id[106]
    id[107] = id[108]
    id[109] = id[110]
    id[111] = id[112]
    id[113] = id[114]
    id[115] = id[116]
    id[117] = id[118]

conn.commit()
conn.close()
