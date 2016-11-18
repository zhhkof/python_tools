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


class Application:
    def __init__(self, root):
        self.root = root
        self.create_frame_bottom()
        self.stopflag = 0
        self.xlsx = Excel()

    def create_frame_bottom(self):

        self.txt0 = tk.Text(self.root, width=160, height=30, border=5)
        self.txt0.pack(side='top')
        self.sl0 = tk.Scrollbar(self.root)
        self.sl0.config(command=self.txt0.yview)
        self.txt0.config(yscrollcommand=self.sl0.set)

        winMC=tk.Frame(self.root, border=4)
        winMC.pack(side='top', anchor='w')

        self.mcgroupid = tk.StringVar(self.root,'224.1.1.10')
        tk.Label(winMC, text='  组播ip： ').pack(side='left')
        tk.Entry(winMC, width='12', textvariable=self.mcgroupid).pack(side='left')

        self.mcport = tk.StringVar(self.root,'4001')
        tk.Label(winMC, text='  组播端口： ').pack(side='left')
        tk.Entry(winMC, width='12', textvariable=self.mcport).pack(side='left')

        win0 = tk.Frame(self.root, border=4)
        win0.pack(side='top', anchor='w')
        win1 = tk.Frame(self.root, border=4)
        win1.pack(side='top', anchor='w')
        win2 = tk.Frame(self.root, border=4)
        win2.pack(side='top', anchor='w')

        wtid = tk.StringVar(self.root)
        tk.Label(win0, text='  风机id： ').pack(side='left')
        # self.wtid = ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(win0, width='12', textvariable=wtid).pack(side='left')

        protocolid = tk.StringVar(self.root, "1178")
        tk.Label(win0, text='  协议号： ').pack(side='left')
        # ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(win0, width='6', textvariable=protocolid).pack(side='left')

        wtstate = tk.StringVar(self.root, '0')
        tk.Label(win0, text='  风机状态： ').pack(side='left')
        # ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(win0, width='6', textvariable=wtstate).pack(side='left')

        error_code = tk.StringVar(self.root, '0')
        tk.Label(win0, text='  故障码： ').pack(side='left')
        # lst3 = ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(win0, width='6', textvariable=error_code).pack(side='left')

        alarm_code = tk.StringVar(self.root, '0')
        tk.Label(win0, text='  警告码： ').pack(side='left')
        # lst4 = ttk.Combobox(win0, values=getValueList(), textvariable=code5, width='6').pack(side='left')
        tk.Entry(win0, width='6', textvariable=alarm_code).pack(side='left')

        power_mode = tk.StringVar(self.root, '0')
        tk.Label(win0, text='  限功率模式字： ').pack(side='left')
        # lst4 = ttk.Combobox(win0, values=getValueList(), textvariable=code5, width='6').pack(side='left')
        tk.Entry(win0, width='6', textvariable=power_mode).pack(side='left')

        stop_mode = tk.StringVar(self.root, '0')
        tk.Label(win0, text='  停机模式字： ').pack(side='left')
        # lst4 = ttk.Combobox(win0, values=getValueList(), textvariable=code5, width='6').pack(side='left')
        tk.Entry(win0, width='6', textvariable=stop_mode).pack(side='left')

        self.bt1 = tk.Button(win0, text='单机单次组播', padx=8, command=lambda: self.send_one(
            [wtid.get(), protocolid.get(), wtstate.get(), error_code.get(), alarm_code.get(), power_mode.get(),
             stop_mode.get()]))
        self.bt1.pack(side='left')

        tk.Label(win1, text='-----------------------' * 6).pack(side='left')

        self.times = tk.StringVar(self.root, '2')
        tk.Label(win2, text='  批量次数： ').pack(side='left')
        tk.Entry(win2, width='4', textvariable=self.times).pack(side='left')

        self.sleepTime = tk.StringVar(self.root, '1')
        tk.Label(win2, text='  间隔时间(s)： ').pack(side='left')
        tk.Entry(win2, width='4', textvariable=self.sleepTime).pack(side='left')

        self.bt2 = tk.Button(win2, text='批量组播', padx=8,
                             command=lambda: self.send_from_xlsx(self.times.get(), self.sleepTime.get()))
        self.bt2.pack(side='left')

        self.bt3 = tk.Button(win2, text='stop', padx=8, command=self.stopkey)
        self.bt3.pack(side='left')

    def send_from_xlsx(self, num, sleepTime):
        self.set_bt_disabled()
        try:
            for i in range(int(num)):
                for msgs in messages_from_xlsx(self.xlsx):
                    if self.stopflag == 1:
                        self.stopflag = 0
                        break
                    for msg in msgs:
                        sender(self.mcgroupid.get(), int(self.mcport.get()), msg)
                        self.txt0.insert(1.0,
                                         datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + msg + "\n")
                        self.txt0.update()
                        time.sleep(int(sleepTime))
            self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                  :-3] + ": " + "-----finish-----" + "\n\r")
        except Exception as e:
            print(e)
        finally:
            self.set_bt_normal()

    def send_one(self, data=[]):
        self.xlsx.loadxlsx()
        seatDict = self.xlsx.get_sNdict_from_sheet()
        wmanModDict = self.xlsx.get_wmanModDict_from_sheet()
        try:
            self.set_bt_disabled()
            for msg in generate_message(data, seatDict, wmanModDict):
                sender(self.mcgroupid.get(), int(self.mcport.get()), msg)
                self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + msg + "\n")
                self.txt0.update()
            self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                  :-3] + ": " + "-----finish-----" + "\n\r")
        except Exception as e:
            print(e)
        finally:
            self.set_bt_normal()

    def set_bt_disabled(self):
        self.bt1.config(state=DISABLED)
        self.bt2.config(state=DISABLED)

    def set_bt_normal(self):
        self.bt1.config(state=NORMAL)
        self.bt2.config(state=NORMAL)

    def stopkey(self):
        self.stopflag = 1


def getValueList():
    args = [1, 2, 3]
    return args


def messages_from_xlsx(xlsx):
    xlsx.loadxlsx()
    datalist = xlsx.get_datalist_from_sheet('info')
    seatDict = xlsx.get_sNdict_from_sheet()
    wmanModDict = xlsx.get_wmanModDict_from_sheet()
    msgs = []
    for data in datalist:
        # msg = []
        # wmanlist = list(wmanlist1178)
        # wmanlist[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # wtid, proid, wtstate, error_code, alarm_code, power_mode_word, stop_mode_word = data
        # seatNums = xlsx.get_sNdict_by_proid().get(proid)
        # wmanlist[seatNums[0] - 1] = wtstate
        # statedata = '(statedata|%s|%s)' % (wtid, wtstate)  # not here, for tcp
        #
        # if power_mode_word != '0':
        #     power_flag = 'true'
        #     wmanlist[seatNums[4] - 1] = power_flag
        #     wmanlist[seatNums[3] - 1] = power_mode_word
        #
        # if stop_mode_word != '0':
        #     wmanlist[seatNums[5] - 1] = stop_mode_word
        # if error_code != '0':
        #     wmanlist[seatNums[1] - 1] = error_code
        #     falutdata = '(falutdata|%s|%s| |2|443c860a-9fe6-4916-9a30-0ecad3821ea2)' % (wtid, error_code)
        #     msg.append(falutdata)
        # if alarm_code != '0':
        #     wmanlist[seatNums[2] - 1] = alarm_code
        #     alarmdata = '(alarmdata|%s|%s| |2)' % (wtid, alarm_code)
        #     msg.append(alarmdata)
        # msg.append('(wman|%s|' % wtid + ','.join(wmanlist))

        msgs.append(generate_message(data, seatDict, wmanModDict))
    return msgs


def generate_message(data, seatDict, wmanModDict):
    # xlsx.loadxlsx()
    msg = []
    wtid, proid, wtstate, error_code, alarm_code, power_mode_word, stop_mode_word = data
    seatNum = seatDict.get(proid)
    # wmanlist = list(wmanlist1178)
    wmanlist = wmanModDict.get(proid)
    wmanlist[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
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
    return msg


root = tk.Tk()
root.title("frontSimulator tool")
a = Application(root)
root.mainloop()
