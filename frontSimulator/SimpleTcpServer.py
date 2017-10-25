import datetime
import socket


class SimpleTcpServer:
    response = ""

    def __init__(self):
        pass

    def start_server(self, host, listen_port, txt_lable):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("*" + host + "*")
        print("*" + str(listen_port) + "*")
        s.bind((host, listen_port))  # 绑定服务ip和端口
        s.listen(10)  # 打开监听,数字大概就是表示可等待连接数。
        while True:
            conn, addr = s.accept()
            print("get request from :", addr)
            data = conn.recv(2048)
            print(data)
            if data.decode('utf-8') == "comtest()":
                conn.sendall("1".encode("utf-8"))
            elif self.response != "":
                conn.sendall(self.response.encode("utf-8"))
            conn.close()  # 1次连接1次数据
            # 界面元素操作得放在后面，不然会影响tcp处理超时。
            txt_lable.insert(1.0,
                             datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                             :-3] + "-receive data from :" + str(addr) + ": " + data.decode('utf-8') + "\n")
            if self.response != "":
                txt_lable.insert(1.0,
                                 datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')[
                                 :-3] + "-send response: " + self.response + "\n")
            txt_lable.update()

    def get_response(self):
        return self.response

    def set_response(self, resp):
        self.response = resp
