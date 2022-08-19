# coding=utf-8
from socket import *
import os,sys

ADDR=('127.0.0.1',9000)
user={}
#登陆
def do_login(s,name,addr):
    #判断登陆
    if name in user or '管理员' in name:
        s.sendto('用户名已经存在'.encode(),addr)
        return
    s.sendto(b'OK',addr)
    #通知其他人
    msg='欢迎%s进入聊天室'%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    #记录用户信息
    user[name]=addr
#聊天
def do_chat(s,name,text):
    msg="%s:%s"%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
#退出
def do_quit(s,name):
    msg="%s退出聊天室"%name
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b"EXIT",user[i])
    #删除用户信息
    del user[name]
#处理请求
def do_request(s):
    while True:
        data,addr=s.recvfrom(1024)
        msg=data.decode().split(' ')
        if msg[0]=="L":
            do_login(s,msg[1],addr)
        elif msg[0]=="C":
            text=' '.join(msg[2:])
            do_chat(s,msg[1],text)
        elif msg[0]=="Q":
            if msg[1] not in user:
                s.sendto(b"EXIT",addr)
                continue
            do_quit(s,msg[1])

def main():
    s=socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)
    pid=os.fork()
    if pid<0:
        return
    elif pid==0:
        while True:
            text=input("管理员消息：")
            msg="C 管理员消息 "+text
            s.sendto(msg.encode(),ADDR)
    else:
        do_request(s)
if __name__=="__main__":
    main()