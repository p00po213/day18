# coding=utf-8
from socket import *
import os,sys

ADDR=('127.0.0.1',9000)


def send_msg(s,name):
    while True:
        try:
            text=input("发言：")
        except KeyboardInterrupt:
            text='quit'
        if text=='quit':
            msg='Q '+name
            s.sendto(msg.encode(),ADDR)
            sys.exit('退出聊天室')
        msg="C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)

def recv_msg(s,name):
    while True:
        msg,addr=s.recvfrom(1024)
        if msg.decode()=="EXIT":
            sys.exit()
        print(msg.decode())

def main():
    s=socket(AF_INET,SOCK_DGRAM)
    while True:
        #登陆
        name=input('请输入姓名：')
        msg="L "+name
        s.sendto(msg.encode(),ADDR)
        data,addr=s.recvfrom(1024)
        if data.decode()=='OK':
            print ("你已经进入了聊天室")
            break
        else:
            print (data.decode())

    pid=os.fork()
    if pid<0:
        sys.exit('Error')
    elif pid==0:
        send_msg(s,name)
    elif pid>0:
        recv_msg(s,name)

if __name__=="__main__":
    main()
