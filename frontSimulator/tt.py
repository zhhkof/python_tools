# coding: utf-8
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox
import time

from frontSimulator.multicastSender import sender
from frontSimulator.xlsxTool import Excel

wmanlist = ['2016-11-10 14:45:08.013', '37.00', 'WTG20', '115/2000', 'Simulator', '150702', '2222_XiaoMing',
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
            '0.00', '0', '1', '', '0']


class Application:
    def __init__(self, root):
        self.root = root
        self.create_frame_bottom()

    def create_frame_bottom(self):
        self.txt0 = tk.Text(self.root, width=160, height=30, border=5)
        self.txt0.pack(side='top')
        win0 = tk.Frame(self.root, border=4)
        win0.pack(side='top', anchor='w')
        win1 = tk.Frame(self.root, border=4)
        win1.pack(side='top', anchor='w')
        win2 = tk.Frame(self.root, border=4)
        win2.pack(side='top', anchor='w')

        # code1 = tk.StringVar(self.root, '1')
        tk.Label(win0, text='  风机id： ').pack(side='left')
        self.wtid = ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')

        code2 = tk.StringVar(self.root, "2")
        tk.Label(win0, text='  代码2： ').pack(side='left')
        ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')

        code3 = tk.StringVar(self.root, '3')
        tk.Label(win0, text='  代码3： ').pack(side='left')
        ttk.Combobox(win0, values=getValueList(), width='6').pack(
            side='left')

        code4 = tk.StringVar(self.root, '1')
        tk.Label(win1, text='  代码4： ').pack(side='left')
        lst3 = ttk.Combobox(win1, values=getValueList(), width='6').pack(side='left')

        code5 = tk.StringVar(self.root)
        tk.Label(win1, text='  代码5： ').pack(side='left')
        lst4 = ttk.Combobox(win1, values=getValueList(), textvariable=code5,
                            width='6').pack(side='left')

        self.times = tk.StringVar(self.root, '2')
        tk.Label(win0, text='  发送次数： ').pack(side='left')
        tk.Entry(win0, width='4', textvariable=self.times).pack(side='left')

        self.bt1=tk.Button(win1, text='单批组播', padx=8, command=lambda: sender('10.80.6.57', 1501, '224.1.1.10', 4001))
        self.bt1.pack(side='left')

        self.bt2=tk.Button(win1, text='全量组播', padx=8, command=lambda: self.send(self.times.get()))
        self.bt2.pack(side='left')

    def send(self,num):
        self.bt2.config(state=DISABLED)
        for i in range(int(num)):
            for msgs in organize_message():
                for msg in msgs:
                    sender('10.80.6.57', 1501, '224.1.1.10', 4001, msg)
                    self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + msg + "\n")
                    self.txt0.update()
                    time.sleep(1)
        self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + "-----finish-----" + "\n\r")
        self.bt2.config(state=NORMAL)


def getValueList():
    args = [1, 2, 3]
    return args


def organize_message():
    xlsx = Excel()
    datalist = xlsx.get_datalist_from_sheet('info')
    msgs = []
    for data in datalist:
        msg = []
        wmanlist[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        wtid = data[0]
        wtstate = data[1]
        wmanlist[21 - 1] = wtstate
        statedata = '(statedata|%s|%s)' % (wtid, wtstate)  # not here, for tcp

        if data[4] != '0':
            power_flag = 'true'
            power_mode_word = data[4]
            wmanlist[269 - 1] = power_flag
            wmanlist[354 - 1] = power_mode_word

        if data[5] != '0':
            stop_mode_word = data[5]
            wmanlist[51 - 1] = stop_mode_word

        if data[2] != '0':
            error_code = data[2]
            wmanlist[347 - 1] = error_code
            falutdata = '(falutdata|%s|%s| |2|443c860a-9fe6-4916-9a30-0ecad3821ea2)' % (wtid, error_code)
            msg.append(falutdata)
        if data[3] != '0':
            alarm_code = data[3]
            wmanlist[346 - 1] = alarm_code
            alarmdata = '(alarmdata|%s|%s| |2)' % (wtid, alarm_code)
            msg.append(alarmdata)
        msg.append('(wman|%s|' % wtid + ','.join(wmanlist))
        msgs.append(msg)
    return msgs


if __name__ == '__main__':
    # for i in organize_message():
    #     print(i)
    root = tk.Tk()
    root.title("tt")
    a = Application(root)
    root.mainloop()
