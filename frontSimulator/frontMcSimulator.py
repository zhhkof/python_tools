# coding: utf-8
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox
import time
import hashlib
from frontSimulator.socketTool import *
from frontSimulator.xlsxTool import Excel
from frontSimulator.FrontTcpServer import TcpServer750
from frontSimulator.SimpleTcpServer import SimpleTcpServer
import threading


class Application:
    def __init__(self, root):
        self.root = root
        # self.frmNoteBook = LabelFrame(self.root, text="功能",border=4)
        # self.frmNoteBook.grid(row=0, column=0, sticky='s' + 'w' + 'e' + 'n')
        note_book = ttk.Notebook(self.root)  # width=1300,height=700
        note_book.grid(row=0, column=0, sticky='s' + 'w' + 'e' + 'n')

        tab_frame1 = tk.Frame(note_book)
        note_book.add(tab_frame1, text='风机状态模拟', padding=1)
        tab_frame2 = tk.Frame(note_book)
        note_book.add(tab_frame2, text='GW750前置模拟', padding=1)
        tab_frame3 = tk.Frame(note_book)
        note_book.add(tab_frame3, text='简易TcpServer', padding=1)

        self.stopflag = 0
        self.xlsx = Excel()
        self.ip_list = get_ipList()

        self.create_front_mc_simulator(tab_frame1)
        self.create_tcp_server_for_gw750(tab_frame2)
        self.create_tcp_server_simple(tab_frame3)

    def create_front_mc_simulator(self, root):
        winTs = tk.Frame(root, border=4)
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

        winMC = tk.Frame(root, border=4)
        winMC.pack(side='top', anchor='w')

        winDiy = tk.Frame(root, border=4)
        winDiy.pack(side='top', anchor='w')

        win1 = tk.Frame(root, border=4)
        win1.pack(side='top', anchor='w')

        win0 = tk.Frame(root, border=4)
        win0.pack(side='top', anchor='w')

        win2 = tk.Frame(root, border=4)
        win2.pack(side='top', anchor='w')

        self.mcgroupid = tk.StringVar(root, '224.1.1.15')
        tk.Label(winMC, text='  组播IP： ').pack(side='left')
        tk.Entry(winMC, width='14', textvariable=self.mcgroupid).pack(side='left')
        self.mcport = tk.IntVar(root, 8769)
        tk.Label(winMC, text='  组播端口： ').pack(side='left')
        tk.Entry(winMC, width='8', textvariable=self.mcport).pack(side='left')

        self.sendip = tk.StringVar(root, self.ip_list[0])
        tk.Label(winMC, text='  本机IP： ').pack(side='left')
        ttk.Combobox(winMC, textvariable=self.sendip, values=self.ip_list, width='14').pack(side='left')
        # tk.Entry(winMC, width='14', textvariable=self.sendip).pack(side='left')

        self.sendport = tk.IntVar(root, 1501)
        tk.Label(winMC, text='  本机发送端口： ').pack(side='left')
        tk.Entry(winMC, width='8', textvariable=self.sendport).pack(side='left')

        self.dds_ip = tk.StringVar(root, '192.168.149.223')
        tk.Label(winMC, text='  数据处理IP： ').pack(side='left')
        tk.Entry(winMC, width='14', textvariable=self.dds_ip).pack(side='left')

        self.dds_port = tk.IntVar(root, 8804)
        tk.Label(winMC, text='  数据处理端口： ').pack(side='left')
        tk.Entry(winMC, width='8', textvariable=self.dds_port).pack(side='left')

        # win1 = tk.Frame(root, border=4)
        # win1.pack(side='top', anchor='w')
        # tk.Label(win1, text='-----------------------' * 8).pack(side='left')

        self.diyMCmsg = tk.StringVar(root)
        tk.Label(winDiy, text='  自定义组播消息： ').pack(side='left')
        tk.Entry(winDiy, width='50', textvariable=self.diyMCmsg).pack(side='left')
        self.bt_diy0 = tk.Button(winDiy, text='发送', padx=8,
                                 command=lambda: self.sendmc_diy(self.diyMCmsg.get(), self.times.get(),
                                                                 self.sleepTime.get()))
        self.bt_diy0.pack(side='left')

        self.diyTCPmsg = tk.StringVar(root)
        tk.Label(winDiy, text='  自定义TCP请求： ').pack(side='left')
        tk.Entry(winDiy, width='50', textvariable=self.diyTCPmsg).pack(side='left')
        self.bt_diy1 = tk.Button(winDiy, text='发送', padx=8, command=lambda: self.sendtcp_diy(self.diyTCPmsg.get()))
        self.bt_diy1.pack(side='left')

        wtid = tk.StringVar(root)
        tk.Label(win0, text='  风机id： ').pack(side='left')
        # ttk.Combobox(win0, textvariable=wtid,values=getValueList(), width='12').pack(side='left')
        tk.Entry(win0, width='10', textvariable=wtid).pack(side='left')

        protocolid = tk.StringVar(root, "1467")
        tk.Label(win0, text='  协议号： ').pack(side='left')
        # ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(win0, width='5', textvariable=protocolid).pack(side='left')

        wtstate = tk.StringVar(root, '0')
        tk.Label(win0, text='  风机状态： ').pack(side='left')
        # ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(win0, width='5', textvariable=wtstate).pack(side='left')

        error_code = tk.StringVar(root, '0')
        tk.Label(win0, text='  故障码： ').pack(side='left')
        # lst3 = ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(win0, width='5', textvariable=error_code).pack(side='left')

        alarm_code = tk.StringVar(root, '0')
        tk.Label(win0, text='  警告码： ').pack(side='left')
        # lst4 = ttk.Combobox(win0, values=getValueList(), textvariable=code5, width='6').pack(side='left')
        tk.Entry(win0, width='5', textvariable=alarm_code).pack(side='left')

        power_mode = tk.StringVar(root, '0')
        tk.Label(win0, text='  限功率模式字： ').pack(side='left')
        # lst4 = ttk.Combobox(win0, values=getValueList(), textvariable=code5, width='6').pack(side='left')
        tk.Entry(win0, width='5', textvariable=power_mode).pack(side='left')

        power_flag = tk.StringVar(root, 'FALSE')
        tk.Label(win0, text='  限功率模标识： ').pack(side='left')
        # lst4 = ttk.Combobox(win0, values=getValueList(), textvariable=code5, width='6').pack(side='left')
        tk.Entry(win0, width='5', textvariable=power_flag).pack(side='left')

        stop_mode = tk.StringVar(root, '0')
        tk.Label(win0, text='  停机模式字： ').pack(side='left')
        # lst4 = ttk.Combobox(win0, values=getValueList(), textvariable=code5, width='6').pack(side='left')
        tk.Entry(win0, width='5', textvariable=stop_mode).pack(side='left')

        self.bt1 = tk.Button(win0, text='单风机数据发送', padx=8, command=lambda: self.send_one(
            {"wtid": wtid.get(), "proid": protocolid.get(), "wtstate": wtstate.get(), "error_code": error_code.get(),
             "alarm_code": alarm_code.get(), "power_mode": power_mode.get(), "power_flag": power_flag.get(),
             "stop_mode": stop_mode.get(), "connect_code": "0"}, self.times.get(), self.sleepTime.get()))
        self.bt1.pack(side='left')

        self.times = tk.StringVar(root, '1')
        tk.Label(win1, text='  组播循环次数： ').pack(side='left')
        ttk.Combobox(win1, values=[1, 5, 10, 20, 30, 40], textvariable=self.times, width='4').pack(side='left')
        # tk.Entry(win2, width='4', textvariable=self.times).pack(side='left')

        self.sleepTime = tk.StringVar(root, '1')
        tk.Label(win1, text='  单条组播间隔(s)： ').pack(side='left')
        tk.Entry(win1, width='4', textvariable=self.sleepTime).pack(side='left')

        self.is_sendtcp = IntVar(root, 0)  # 1-select,0-unselect
        tk.Checkbutton(win1, text='组播时发送对应tcp请求(仅一次，自定义不生效)|      ', variable=self.is_sendtcp).pack(side='left')

        # multicast file choose button
        self.multicast_file_choose_btn = tk.Button(win1, text="自定义组播文件：",
                                                   command=lambda: open_file(self.multicast_file_path))
        self.multicast_file_choose_btn.pack(side='left')

        # file path Entry
        self.multicast_file_path = StringVar()
        self.entry_multicast_file = tk.Entry(win1, width=10, textvariable=self.multicast_file_path)
        self.entry_multicast_file.pack(side='left')

        # multicast file send button
        self.multicast_file_send_btn = tk.Button(win1, text="开始发送",
                                                 command=lambda: self.sendmc_diy_from_file(
                                                     self.multicast_file_path.get(), self.times.get(),
                                                     self.sleepTime.get()))
        self.multicast_file_send_btn.pack(side='left')

        # tk.Label(win1, text='-----------------------' * 6).pack(side='left')

        self.bt2 = tk.Button(win2, text='批量Excel数据发送', padx=8,
                             command=lambda: do_with_thread(lambda:
                                                            self.send_from_xlsx(self.times.get(),
                                                                                self.sleepTime.get())))
        self.bt2.pack(side='left')

        self.bt3 = tk.Button(win2, text='Stop', padx=8, command=self.stopSend)
        self.bt3.pack(side='left')
        self.bt4 = tk.Button(win2, text='Clear', padx=8, command=self.clearText)
        self.bt4.pack(side='left')

    def create_tcp_server_for_gw750(self, root):
        server_frame = tk.Frame(root, border=4)
        server_frame.pack(side='top', anchor='w')

        server_ip = tk.StringVar(root, self.ip_list[0])
        tk.Label(server_frame, text='  服务ip： ').pack(side='left')
        ttk.Combobox(server_frame, textvariable=server_ip, values=self.ip_list, width='14').pack(side='left')

        port = tk.IntVar(root, 8801)
        tk.Label(server_frame, text='  端口： ').pack(side='left')
        # ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(server_frame, width='6', textvariable=port).pack(side='left')
        # button_start_server = tk.Button(server_frame, text='start', padx=8,
        #                                 command=lambda: TcpServer750(server_ip.get(), port.get()).start())
        button_start_server = tk.Button(server_frame, text='start', padx=8,
                                        command=lambda: do_with_thread(TcpServer750(server_ip.get(), port.get()).run))
        button_start_server.pack(side='left')

        button_check_server = tk.Button(server_frame, text='check server', padx=8,
                                        command=lambda: self.getServerState(root, server_state, server_ip.get(),
                                                                            port.get()))
        button_check_server.pack(side='left')

        server_state = tk.Label(server_frame)
        server_state.pack(side='left')

    def create_tcp_server_simple(self, root):
        server_frame = tk.Frame(root, border=4)
        server_frame.pack(side='top', anchor='w')

        lable_frame = tk.Frame(root, border=4)
        lable_frame.pack(side='top', anchor='w')

        server_ip = tk.StringVar(root, self.ip_list[0])
        tk.Label(server_frame, text='  服务ip： ').pack(side='left')
        ttk.Combobox(server_frame, textvariable=server_ip, values=self.ip_list, width='14').pack(side='left')

        port = tk.IntVar(root, 60000)
        tk.Label(server_frame, text='  端口： ').pack(side='left')
        # ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(server_frame, width='6', textvariable=port).pack(side='left')
        # button_start_server = tk.Button(server_frame, text='start', padx=8,
        #                                 command=lambda: TcpServer750(server_ip.get(), port.get()).start())

        sts = SimpleTcpServer()
        button_start_server = tk.Button(server_frame, text='start', padx=8,
                                        command=lambda: do_with_thread_args(sts.start_server,
                                                                            (server_ip.get(), port.get(), txt0)))
        button_start_server.pack(side='left')

        button_check_server = tk.Button(server_frame, text='check server', padx=8,
                                        command=lambda: self.getServerState(root, server_state, server_ip.get(),
                                                                            port.get()))
        button_check_server.pack(side='left')
        server_state = tk.Label(server_frame)
        server_state.pack(side='left')
        resp = tk.StringVar(root, "")
        tk.Label(server_frame, text='  返回值： ').pack(side='left')
        # ttk.Combobox(win0, values=getValueList(), width='6').pack(side='left')
        tk.Entry(server_frame, width='6', textvariable=resp).pack(side='left')

        button_set_resp = tk.Button(server_frame, text='生效', padx=8,
                                    command=lambda: sts.set_response(resp.get()))
        button_set_resp.pack(side='left')

        txt0 = tk.Text(lable_frame, width=150, height=30, border=5, wrap='none')
        sly = tk.Scrollbar(lable_frame, orient=tk.VERTICAL)
        sly.config(command=txt0.yview)
        slx = tk.Scrollbar(lable_frame, orient=tk.HORIZONTAL)
        slx.config(command=txt0.xview)
        txt0.config(yscrollcommand=sly.set, xscrollcommand=slx.set)
        # layout
        sly.pack(side='right', fill='y', expand=0, anchor=N)
        slx.pack(side='bottom', fill='x', expand=0, anchor=N)
        txt0.pack(side='left', expand=1, fill='x')

    def send_from_xlsx(self, num, sleepTime):
        self.set_bt_disabled()
        messages = messages_from_xlsx2(self.xlsx)
        try:
            self.stopflag = 0
            for i in range(int(num)):
                for msgs in messages:
                    if self.stopflag == 1:
                        break
                    # tcp单次请求
                    if i == 0 and len(msgs['tcp']) > 0 and self.is_sendtcp.get() == 1:
                        for tcpmsg in msgs['tcp']:
                            tcp_result = tcp_send(self.dds_ip.get(), self.dds_port.get(), tcpmsg)
                            self.txt0.insert(1.0,
                                             datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                             :-3] + ": " + tcp_result + "\n")
                            self.txt0.update()
                    # 组播循环
                    for msg in msgs['multicast']:
                        if self.stopflag == 1:
                            break
                        multicast_send(self.sendip.get(), self.sendport.get(), self.mcgroupid.get(),
                                       self.mcport.get(), msg)
                        self.txt0.insert(1.0,
                                         datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + msg + "\n")
                        self.txt0.update()
                        time.sleep(float(sleepTime))
            self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                  :-3] + ": " + "-----finish-----" + "\n")
        except Exception as e:
            print(e)
        finally:
            self.stopflag = 0
            self.set_bt_normal()

    def send_one(self, dataDict={}, num='1', sleepTime='1'):
        self.xlsx.loadxlsx()
        seatDict = self.xlsx.get_sNdict_from_sheet()
        wmanModDict = self.xlsx.get_wmanModDict_from_sheet()
        msgs = generate_message2(dataDict, seatDict, wmanModDict)
        try:
            self.set_bt_disabled()
            self.stopflag = 0
            for i in range(int(num)):
                if self.stopflag == 1:
                    break
                if i == 0 and len(msgs['tcp']) > 0 and self.is_sendtcp.get() == 1:
                    for tcpmsg in msgs['tcp']:
                        tcp_result = tcp_send(self.dds_ip.get(), self.dds_port.get(), tcpmsg)
                        self.txt0.insert(1.0,
                                         datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                         :-3] + ": " + tcp_result + "\n")
                        self.txt0.update()
                for msg in msgs['multicast']:
                    if self.stopflag == 1:
                        break
                    multicast_send(self.sendip.get(), self.sendport.get(), self.mcgroupid.get(),
                                   self.mcport.get(), msg)
                    self.txt0.insert(1.0,
                                     datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + msg + "\n")
                    self.txt0.update()
                    time.sleep(float(sleepTime))
            self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                  :-3] + ": " + "-----finish-----" + "\n")
        except Exception as e:
            print(e)
        finally:
            self.stopflag = 0
            self.set_bt_normal()

    def sendmc_diy(self, msg, num='1', sleepTime='1'):
        try:
            self.set_bt_disabled()
            self.stopflag = 0
            for i in range(int(num)):
                if self.stopflag == 1:
                    break
                multicast_send(self.sendip.get(), self.sendport.get(), self.mcgroupid.get(), self.mcport.get(),
                               msg)
                self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + msg + "\n")
                self.txt0.update()
                time.sleep(float(sleepTime))

            self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                  :-3] + ": " + "-----finish-----" + "\n")
        except Exception as e:
            print(e)
        finally:
            self.stopflag = 0
            self.set_bt_normal()

    def sendmc_diy_from_file(self, file_path, num='1', sleepTime='1'):
        try:
            self.set_bt_disabled()
            self.stopflag = 0
            file = open(file_path, "r")
            lines = file.readlines()
            for i in range(int(num)):
                for msg in lines:
                    if self.stopflag == 1:
                        break
                    msg = msg.strip()
                    multicast_send(self.sendip.get(), self.sendport.get(), self.mcgroupid.get(), self.mcport.get(),
                                   msg)
                    self.txt0.insert(1.0,
                                     datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + msg + "\n")
                    self.txt0.update()
                    time.sleep(float(sleepTime))
            self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                  :-3] + ": " + "-----finish-----" + "\n")
        except Exception as e:
            print(e)
        finally:
            file.close()
            self.stopflag = 0
            self.set_bt_normal()

    def sendtcp_diy(self, msg):
        self.set_bt_disabled()
        tcp_result = tcp_send(self.dds_ip.get(), self.dds_port.get(), msg)  # 超时设置1秒
        self.txt0.insert(1.0, datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[:-3] + ": " + tcp_result + "\n")
        self.txt0.update()
        self.set_bt_normal()

    def set_bt_disabled(self):
        self.bt_diy0.config(state=DISABLED)
        self.bt_diy1.config(state=DISABLED)
        self.bt1.config(state=DISABLED)
        self.bt2.config(state=DISABLED)
        self.multicast_file_send_btn.config(state=DISABLED)

    def set_bt_normal(self):
        self.bt_diy0.config(state=NORMAL)
        self.bt_diy1.config(state=NORMAL)
        self.bt1.config(state=NORMAL)
        self.bt2.config(state=NORMAL)
        self.multicast_file_send_btn.config(state=NORMAL)

    def stopSend(self):
        self.stopflag = 1

    def clearText(self):
        self.txt0.delete(0.0, END)

    def getServerState(self, root, label, server_ip, port):
        res = 'No run'
        if isServerStart(server_ip, port):
            res = 'Running..'
        label['text'] = res
        root.update()


def messages_from_xlsx2(xlsx):
    xlsx.loadxlsx()
    datalist2 = xlsx.get_datalist_from_sheet2()  # 从xlsx中获取所有行为list
    seatDict = xlsx.get_sNdict_from_sheet()
    wmanModDict = xlsx.get_wmanModDict_from_sheet()
    msgs = []
    for datadict in datalist2:
        msgdict = generate_message2(datadict, seatDict, wmanModDict)
        msgs.append(msgdict)
    return msgs


# 根据行记录或ui输入记录生成单风机的发送数据
def generate_message2(datadict, seatDict, wmanModDict):
    # xlsx.loadxlsx()
    msgdict = {'multicast': [], 'tcp': []}  # 单风机数据dict，key:multicast,tcp
    # msg = []
    for key in datadict:
        exec(key + "='" + datadict.get(key) + "'", globals())
        print(key + ":" + datadict.get(key))
    if connect_code != '0':
        comstate = "(comstate|%s|%s)" % (wtid, connect_code)
        # msg.append(comstate)
        msgdict['multicast'].append(comstate)
    else:
        seatNum = seatDict.get(proid)
        # print(seatNum)
        # wmanlist = list(wmanlist1178)
        wmanlist = list(wmanModDict.get(proid))  # 一定要加list(),否则不是新对象，会导致后面循环采用前面的list。
        # print(wmanlist)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        wmanlist[0] = now_time
        if proid == '1104':
            wmanlist[1] = wmanlist[0]
        wmanlist[seatNum[0] - 1] = wtstate
        wmanlist[seatNum[4] - 1] = power_flag
        statedata = '(statedata|%s|%s)' % (wtid, wtstate)  # not here, for tcp
        msgdict['tcp'].append(statedata)
        if power_mode != '0':
            # power_flag = 'true'
            # wmanlist[seatNum[4] - 1] = power_flag
            wmanlist[seatNum[3] - 1] = power_mode

        if stop_mode != '0':
            wmanlist[seatNum[5] - 1] = stop_mode
        if error_code != '0':
            wmanlist[seatNum[1] - 1] = error_code
            falutdata = '(falutdata|%s|%s| |2|%s)' % (
                wtid, error_code, generate_unique_code(wtid + error_code + now_time))
            # msg.append(falutdata)
            msgdict['multicast'].append(falutdata)
            msgdict['tcp'].append(falutdata)
        if alarm_code != '0':
            wmanlist[seatNum[2] - 1] = alarm_code
            alarmdata = '(alarmdata|%s|%s| |2)' % (wtid, alarm_code)
            # msg.append(alarmdata)
            msgdict['multicast'].append(alarmdata)
            msgdict['tcp'].append(alarmdata)
        # msg.append('(wman|%s|' % wtid + ','.join(wmanlist) + ')')
        msgdict['multicast'].append('(wman|%s|' % wtid + ','.join(wmanlist) + ')')
    # print(msgdict)
    return msgdict


def do_with_thread(func):
    t1 = threading.Thread(target=func)
    t1.setDaemon(True)
    t1.start()


def do_with_thread_args(func, args):
    t1 = threading.Thread(target=func, args=args)
    t1.setDaemon(True)
    t1.start()


def open_file(entry_text):
    fname = filedialog.askopenfilename(
        filetypes=(("source files", "*.txt"), ("All files", "*.*")))
    entry_text.set(fname)


# def get_tcpserver_for_gw750(host, port):
#     return TcpServer750(host, port)


# def getValueList(xlsx):
#     xlsx.loadxlsx()
#
#     return args

##老方法
# def messages_from_xlsx(xlsx):
#     xlsx.loadxlsx()
#     datalist = xlsx.get_datalist_from_sheet()
#     datalist2 = xlsx.get_datalist_from_sheet2()
#     seatDict = xlsx.get_sNdict_from_sheet()
#     wmanModDict = xlsx.get_wmanModDict_from_sheet()
#     msgs = []
#     for data in datalist:
#         msgs.append(generate_message(data, seatDict, wmanModDict))
#     return msgs
#
#
# def generate_message(data, seatDict, wmanModDict):
#     # xlsx.loadxlsx()
#     msg = []
#     wtid, proid, wtstate, error_code, alarm_code, power_mode_word, stop_mode_word, connect_code = data
#     if connect_code != '0':
#         comstate = "(comstate|%s|%s)" % (wtid, connect_code)
#         msg.append(comstate)
#         return msg
#     seatNum = seatDict.get(proid)
#     # wmanlist = list(wmanlist1178)
#     wmanlist = list(wmanModDict.get(proid))
#     wmanlist[0] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
#     wmanlist[seatNum[0] - 1] = wtstate
#     statedata = '(statedata|%s|%s)' % (wtid, wtstate)  # not here, for tcp
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
#
#     if power_mode_word != '0':
#         power_flag = 'true'
#         wmanlist[seatNum[4] - 1] = power_flag
#         wmanlist[seatNum[3] - 1] = power_mode_word
#
#     if stop_mode_word != '0':
#         wmanlist[seatNum[5] - 1] = stop_mode_word
#     if error_code != '0':
#         wmanlist[seatNum[1] - 1] = error_code
#         falutdata = '(falutdata|%s|%s| |2|%s)' % (wtid, error_code, generate_unique_code(wtid + error_code + now_time))
#         msg.append(falutdata)
#     if alarm_code != '0':
#         wmanlist[seatNum[2] - 1] = alarm_code
#         alarmdata = '(alarmdata|%s|%s| |2)' % (wtid, alarm_code)
#         msg.append(alarmdata)
#     msg.append('(wman|%s|' % wtid + ','.join(wmanlist) + ')')
#     return msg


def generate_unique_code(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    l = list(m.hexdigest())
    l[7] += '-'
    l[11] += '-'
    l[15] += '-'
    l[19] += '-'
    return ''.join(l)


root = tk.Tk()
root.title("风机状态模拟信息组播/tcp发送工具")
a = Application(root)
root.mainloop()
