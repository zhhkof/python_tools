# coding:utf-8
import time
import struct
from socket import *


# 发送端本机ip和端口
# SENDERIP = '192.168.149.12'
# SENDERPORT = 1501

# 组播地址端口等
# MYPORT = 1600
# MYGROUP = '224.1.1.10'
# MYTTL = 255


def multicast_send(SENDERIP, SENDERPORT, MYGROUP, MYPORT, SENDDATA='testdata'):
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    s.bind((SENDERIP, SENDERPORT))  # 这句注释掉都可以。发送端口会被自动分配。
    # Set Time-to-live (optional)
    ttl_bin = struct.pack('@i', 255)
    s.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl_bin)
    status = s.setsockopt(IPPROTO_IP,
                          IP_ADD_MEMBERSHIP,
                          inet_aton(MYGROUP) + inet_aton(SENDERIP))  # 加入组播组
    # for i in range(times):
    # data = (time.strftime('%Y-%m-%d %H:%M:%S') + ': multicast test data.').encode('utf-8')  # socket发送需转成byte字节。
    s.sendto(SENDDATA.encode('utf-8'), (MYGROUP, MYPORT))
    # print(str(i) + ":" + SENDDATA)
    print("send data ok !")
    # time.sleep(1)

def multicast_send2(**kwargs):
    if 'SENDERIP' in kwargs.keys():
        print(kwargs['SENDERIP'])
    if 'SENDERPORT' in kwargs.keys():
        print(kwargs['SENDERPORT'])
multicast_send2(SENDERIP=1)

# HOST = '192.168.149.223'
# PORT = 8804


def tcp_send(HOST, PORT, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(data.encode("utf-8"))
    # print("send data:"+data)
    resp = s.recv(1024)
    # print("response:", resp.decode('utf-8'))
    result = "send data: " + data + " | " + "response:" + resp.decode('utf-8')
    s.close()
    return result


def get_ipList():
    try:
        iplist = gethostbyname_ex(gethostname())[2]
        return iplist
    except Exception:
        return []
