# coding: utf-8
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox
import time
import hashlib
from frontSimulator.multicastSender import sender
from frontSimulator.xlsxTool import Excel
import threading


class Application:
    def __init__(self, root):
        self.root = root
        self.create_frame_bottom()
        self.stopflag = 0
        self.xlsx = Excel()

    def create_frame_bottom(self):
        winTs = tk.Frame(self.root, border=4)
        winTs.pack(side='top', anchor='w')
        self.txt0 = tk.Text(winTs, width=160, height=30, border=5, wrap='none')
        self.sly = tk.Scrollbar(winTs, orient=tk.VERTICAL)
        self.sly.config(command=self.txt0.yview)
        self.slx = tk.Scrollbar(winTs, orient=tk.HORIZONTAL)
        self.slx.config(command=self.txt0.xview)
        self.txt0.config(yscrollcommand=self.sly.set, xscrollcommand=self.slx.set)
        # layout
        self.sly.pack(side='right', fill='y', expand=0, anchor=N)
        self.slx.pack(side='bottom', fill='x', expand=0, anchor=N)
        self.txt0.pack(side='left', expand=1, fill='x')

        winMC = tk.Frame(self.root, border=4)
        winMC.pack(side='top', anchor='w')
        self.mcgroupid = tk.StringVar(self.root, '224.1.1.15')
        tk.Label(winMC, text='  组播ip： ').pack(side='left')
        tk.Entry(winMC, width='12', textvariable=self.mcgroupid).pack(side='left')
        self.mcport = tk.StringVar(self.root, '8769')
        tk.Label(winMC, text='  组播端口： ').pack(side='left')
        tk.Entry(winMC, width='12', textvariable=self.mcport).pack(side='left')
        self.diyMCmsg = tk.StringVar(self.root)
        tk.Label(winMC, text='  DIY组播消息： ').pack(side='left')
        tk.Entry(winMC, width='67', textvariable=self.diyMCmsg).pack(side='left')
        self.bt0 = tk.Button(winMC, text='DIY消息发送', padx=8, command=lambda: self.send_diy(self.diyMCmsg.get()))
        self.bt0.pack(side='left')

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

        self.times = tk.StringVar(self.root, '1')
        tk.Label(win2, text='  批量次数： ').pack(side='left')
        ttk.Combobox(win2, values=[1,5,10,20,30,40], textvariable=self.times, width='4').pack(side='left')
        # tk.Entry(win2, width='4', textvariable=self.times).pack(side='left')

        self.sleepTime = tk.StringVar(self.root, '0')
        tk.Label(win2, text='  间隔时间(s)： ').pack(side='left')
        tk.Entry(win2, width='4', textvariable=self.sleepTime).pack(side='left')

        self.bt2 = tk.Button(win2, text='批量组播', padx=8,
                             command=lambda: do_with_thread(
                                 self.send_from_xlsx(self.times.get(), self.sleepTime.get())))
        self.bt2.pack(side='left')

        self.bt3 = tk.Button(win2, text='Stop', padx=8, command=self.stopSend)
        self.bt3.pack(side='left')
        self.bt4 = tk.Button(win2, text='Clear', padx=8, command=self.clearText)
        self.bt4.pack(side='right')

    def send_from_xlsx(self, num, sleepTime):
        self.set_bt_disabled()
        try:
            for i in range(int(num)):
                if self.stopflag == 1:
                    break
                for msgs in messages_from_xlsx2(self.xlsx):
                    if self.stopflag == 1:
                        break
                    for msg in msgs:
                        if self.stopflag == 1:
                            break
                        sender(self.mcgroupid.get(), int(self.mcport.get()), msg)
                        self.txt0.insert(1.0,
                                         datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + msg + "\n")
                        self.txt0.update()
                        time.sleep(int(sleepTime))
            self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                  :-3] + ": " + "-----finish-----" + "\n")
        except Exception as e:
            print(e)
        finally:
            self.stopflag = 0
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

    def send_diy(self, msg):
        try:
            self.set_bt_disabled()
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
        self.bt0.config(state=DISABLED)
        self.bt1.config(state=DISABLED)
        self.bt2.config(state=DISABLED)

    def set_bt_normal(self):
        self.bt0.config(state=NORMAL)
        self.bt1.config(state=NORMAL)
        self.bt2.config(state=NORMAL)

    def stopSend(self):
        self.stopflag = 1

    def clearText(self):
        self.txt0.delete(0.0, END)

def messages_from_xlsx2(xlsx):
    xlsx.loadxlsx()
    datalist2 = xlsx.get_datalist_from_sheet2()
    seatDict = xlsx.get_sNdict_from_sheet()
    wmanModDict = xlsx.get_wmanModDict_from_sheet()
    msgs = []
    for datadict in datalist2:
        msgs.append(generate_message2(datadict, seatDict, wmanModDict))
    # print(msgs)
    # print(msgs)
    return msgs

def generate_message2(datadict, seatDict, wmanModDict):
    # xlsx.loadxlsx()
    msg = []
    for key in datadict:
        exec(key + "='" + datadict.get(key) + "'", globals())
        # print(key+":"+datadict.get(key))
    if connect_code != '0':
        comstate = "(comstate|%s|%s)" % (wtid, connect_code)
        msg.append(comstate)
    else:
        seatNum = seatDict.get(proid)
        # wmanlist = list(wmanlist1178)
        wmanlist = list(wmanModDict.get(proid)) #一定要加list(),否则不是新对象，会导致后面循环采用前面的list。
        # print(wmanlist)
        wmanlist[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        wmanlist[seatNum[0] - 1] = wtstate
        statedata = '(statedata|%s|%s)' % (wtid, wtstate)  # not here, for tcp

        if power_mode != '0':
            power_flag = 'true'
            wmanlist[seatNum[4] - 1] = power_flag
            wmanlist[seatNum[3] - 1] = power_mode

        if stop_mode != '0':
            wmanlist[seatNum[5] - 1] = stop_mode
        if error_code != '0':
            wmanlist[seatNum[1] - 1] = error_code
            falutdata = '(falutdata|%s|%s| |2|%s)' % (wtid, error_code, generate_unique_code(wtid + error_code))
            msg.append(falutdata)
        if alarm_code != '0':
            wmanlist[seatNum[2] - 1] = alarm_code
            alarmdata = '(alarmdata|%s|%s| |2)' % (wtid, alarm_code)
            msg.append(alarmdata)
        msg.append('(wman|%s|' % wtid + ','.join(wmanlist))
    return msg


def do_with_thread(func):
    t1 = threading.Thread(target=func)
    t1.setDaemon(True)
    t1.start()


def getValueList():
    args = [1, 2, 3]
    return args


def messages_from_xlsx(xlsx):
    xlsx.loadxlsx()
    datalist = xlsx.get_datalist_from_sheet()
    datalist2 = xlsx.get_datalist_from_sheet2()
    seatDict = xlsx.get_sNdict_from_sheet()
    wmanModDict = xlsx.get_wmanModDict_from_sheet()
    msgs = []
    for data in datalist:
        msgs.append(generate_message(data, seatDict, wmanModDict))
    return msgs


def generate_message(data, seatDict, wmanModDict):
    # xlsx.loadxlsx()
    msg = []
    wtid, proid, wtstate, error_code, alarm_code, power_mode_word, stop_mode_word,connect_code = data
    if connect_code != '0':
        comstate = "(comstate|%s|%s)" % (wtid, connect_code)
        msg.append(comstate)
        return msg
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
        falutdata = '(falutdata|%s|%s| |2|%s)' % (wtid, error_code, generate_unique_code(wtid + error_code))
        msg.append(falutdata)
    if alarm_code != '0':
        wmanlist[seatNum[2] - 1] = alarm_code
        alarmdata = '(alarmdata|%s|%s| |2)' % (wtid, alarm_code)
        msg.append(alarmdata)
    msg.append('(wman|%s|' % wtid + ','.join(wmanlist))
    return msg


def generate_unique_code(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    l = list(m.hexdigest())
    l[7] += '-'
    l[11] += '-'
    l[15] += '-'
    return ''.join(l)


root = tk.Tk()
root.title("frontSimulator tool")
a = Application(root)
root.mainloop()
