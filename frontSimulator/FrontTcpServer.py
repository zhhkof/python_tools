import socket, time, random
from frontSimulator.xlsxTool import Excel
import threading


# GW750机型前置tcpserver模拟
class TcpServer750(threading.Thread):
    def __init__(self, host, listen_prot):
        super().__init__()
        self.xlsx = Excel()
        self.host = host
        self.listen_port = listen_prot

    def run(self):
        # host = '10.80.10.248'
        # listen_port = 7777
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.listen_port))  # 绑定服务ip和端口
        s.listen(10)  # 打开监听,数字大概就是表示可等待连接数。
        while True:
            conn, addr = s.accept()
            print("get request from :", addr)
            data = conn.recv(1024)
            print(data)
            conn.sendall(self.get_response(data.decode('utf-8')).encode("utf-8"))
            conn.close()  # 1次连接1次数据

    def get_response(self, request):
        if request.startswith('getpackdata'):
            self.xlsx.loadxlsx()
            packages = self.xlsx.get_Package_data_from_sheet()
            package_name = request.split('|')[0].split('(')[1]
            wtid = request.split('|')[1]
            reslist = packages[wtid + '|' + package_name]
            return '(' + ",".join(reslist) + ')'
        else:
            return request + "***error input***"


if __name__ == '__main__':
    e = TcpServer750('10.80.10.248', 7777)
