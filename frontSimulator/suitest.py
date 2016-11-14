# coding: utf-8
# import datetime
# from tkinter import *
# from tkinter import ttk
# from tkinter import filedialog
# import tkinter as tk
# import tkinter.messagebox as messagebox
# import time
#
# root = tk.Tk()
# txt0 = tk.Text(root, width=80, height=24, border=5)
# txt0.pack(side='top')
# win0 = tk.Frame(root, border=4)
# win0.pack(side='top', anchor='w')
# win1 = tk.Frame(root, border=4)
# win1.pack(side='top', anchor='w')
#
#
# # i=0
# def text():
#     # global i
#     # i += 1
#     t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#     txt0.insert(1.0, t + ":456\n")
#     # txt0.insert(1.0, time.strftime('%Y-%m-%d %H:%M:%S')+":456\n")
#
#
# comx = tk.StringVar(root, 'COM1')
# tk.Label(win0, text='串口号： ').pack(side='left')
# ttk.Combobox(win0, text=comx, values=['COM1', 'COM2', 'COM3'], width='12').pack(side='left')
#
# baud = tk.StringVar(root, "9600")
# tk.Label(win0, text='  波特率： ').pack(side='left')
# ttk.Combobox(win0, textvariable=baud, values=['4800', '9600', '19200'], width='12').pack(side='left')
#
# tk.Button(win0, text='打开串口', padx=8, command=text).pack(side='left')
#
# dlen = tk.StringVar(root, '8')
# tk.Label(win1, text='数据位： ').pack(side='left')
# ttk.Combobox(win1, textvariable=dlen, values=['9', '8', '7', '6', '5,', '4'], width='12').pack(side='left')
#
# slen = tk.StringVar(root, '1')
# tk.Label(win1, text='  停止位： ').pack(side='left')
# lst3 = ttk.Combobox(win1, textvariable=slen, values=['1', '2'], width='12').pack(side='left')
#
# chck = tk.StringVar(root, 'None')
# tk.Label(win1, text='  校验位： ').pack(side='left')
# lst4 = ttk.Combobox(win1, textvariable=chck, values=['None', 'Odd', 'Even', 'Mark', 'Space'], width='12').pack(
#     side='left')
#
#
#
#
#
# root.mainloop()
from frontSimulator.xlsxTool import Excel
import datetime
wmanlist1178 = ('2016-11-10 14:45:08.013', '37.00', 'WTG20', '115/2000', 'Simulator', '150702', '2222_XiaoMing',
                '192.168.137.1.1.1', 'GW_V_GL', '2015-07-02 00:00:00.000', 'SW66.6_V20150702', '20065', '', '16',
                '2016', '11', '10', '14', '45', '7', '2', '600', '0', '37', '34', '28', '65', '39', '43', '26', '38',
                '0', '0', '0', '0', '0', '0', '0.00', '0.00', '0.00', '0', '0', '0', '0', '0', '0', '0', '0', '0', '',
                '', '', '', '', '', '0', '0', '0', '0', '5', '2', '7', '3', '2060', '6', '0', '0', '0', '6', '7', '2',
                '1', '2', '0', '3', '20071', '6', '103.60', '10.36', '16.22', '0.00', '0.00', '8.84', '77.03', '2.62',
                '0.00', '0.00', '0.00', '20.16', '8.84', '23.95', '79.65', '2.50', '65.70', '63.20', '0.00',
                '-1801801.00', '0.00', '0.01', '0.01', '0.01', '3.00', '0.00', '275.94', '275.94', '275.94', '60.00',
                '-0.50', '-0.50', '0.49', '0.00', '55.00', '50.00', '36.00', '44.00', '52.00', '53.00', '275.94',
                '0.00', '0.00', '527582877.92', '682.00', '693.00', '692.00', '0.02', '0.02', '693.00', '0.00', '49.00',
                '-414.00', '0.88', '45.00', '35.00', '26.00', '34.00', '67.00', '36.00', '25.00', '44.00', '40.00',
                '37.00', '51.00', '58.00', '56.00', '40.00', '65.00', '40.00', '62.00', '42.00', '60.00', '699.00',
                '693.00', '690.00', '387.00', '399.00', '388.00', '63.70', '-538.20', '1.14', '0.00', '0.00', '0.00',
                '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '109.56', '16.35', '16.21', '29.94', '14.84',
                '20071.00', '138.00', '0.00', '0.00', '29.00', '0.00', '0.00', '0.00', '0.00', '681.00', '0.00',
                '62.00', '41.00', '125.00', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'false', 'true', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'true', '125.00', '172.99', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', 'true', 'true', 'false', 'false', 'false', 'false', 'false', 'false', 'false',
                'false', 'false', 'true', 'false', 'false', 'false', 'false', 'false', 'false', '0.00', '0.00', '0.00',
                '0.00', '0.00', '0.00', '0.00', 'false', '', '', '', '', '', '', '', '0', '0', 'UnLock', 'False', '0',
                '0.00', '0', '1', '', '0')

def organize_messages():
    xlsx = Excel()
    datalist = xlsx.get_datalist_from_sheet('info')
    msgs = []
    for data in datalist:
        msg = []
        wmanlist = list(wmanlist1178)
        wmanlist[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # wtid = data[0]
        # proid= data[1]
        # wtstate = data[2]
        # error_code = data[3]
        # alarm_code = data[4]
        # power_mode_word = data[5]
        # stop_mode_word = data[6]
        print(data)
        wtid, proid, wtstate, error_code, alarm_code, power_mode_word, stop_mode_word = data
        seatNum = xlsx.get_sNdict_by_proid().get(proid)
        print(seatNum)
        wmanlist[seatNum[0] - 1] = wtstate
        statedata = '(statedata|%s|%s)' % (wtid, wtstate)  # not here, for tcp

        if power_mode_word != '0':
            power_flag = 'true'
            wmanlist[seatNum[4] - 1] = power_flag
            wmanlist[seatNum[3] - 1] = power_mode_word

        if stop_mode_word != '0':
            wmanlist[seatNum[5] - 1] = stop_mode_word
        if error_code != '0':
            wmanlist[seatNum[1] - 1] = error_code
            falutdata = '(falutdata|%s|%s| |2|443c860a-9fe6-4916-9a30-0ecad3821ea2)' % (wtid, error_code)
            msg.append(falutdata)
        if alarm_code != '0':
            wmanlist[seatNum[2] - 1] = alarm_code
            alarmdata = '(alarmdata|%s|%s| |2)' % (wtid, alarm_code)
            msg.append(alarmdata)
        msg.append('(wman|%s|' % wtid + ','.join(wmanlist))
        print(msg)
        print('------------------------------')
        msgs.append(msg)
    print(wmanlist1178)


organize_messages()
print(wmanlist1178)