# coding=utf-8
"""
dict服务端部分
处理请求逻辑
"""
from socket import *
from multiprocessing import Process
import signal
import sys
from operate_db import *
from time import sleep

#全局变量
HOST='127.0.0.1'
PORT=9000
ADDR=(HOST,PORT)

#处理注册
def do_register(c,db,data):
    tmp=data.split(" ")
    name=tmp[1]
    passwd=tmp[2]
    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')
#处理登陆
def do_login(c,db,data):
    tmp=data.split(" ")
    name=tmp[1]
    passwd=tmp[2]
    if db.login(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')
#查询单词
def do_query(c,db,data):
    tmp=data.split(" ")
    name=tmp[1]
    word=tmp[2]

    #插入历史记录
    db.insert_history(name,word)
    mean=db.query(word)
    if not mean:
        c.send("单词没找到".encode())
    else:
        msg='%s:%s'%(word,mean)
        c.send(msg.encode())

def do_history(c,db,data):
    tmp=data.split(" ")
    name=tmp[1]
    result=db.search_history(name)
    if not result:
        c.send(b'Fail')
        return
    c.send(b'OK')
    sleep(0.1)
    for item in result:
        msg="%d  %s  %s   %s\n"%item
        c.send(msg.encode())
    sleep(0.1)
    c.send(b'##')


#处理客户端请求
def do_request(c,db):
    db.create_cursor()  #生成游标
    while True:
        addr=c.getpeername()
        data=c.recv(1024).decode()
        if not data or data[0]=='E':
            c.close()
            sys.exit('客户端退出'+str(addr))
        if data[0]=='R':
            do_register(c,db,data)
        if data[0]=='L':
            do_login(c,db,data)
        if data[0]=='Q':
            do_query(c,db,data)
        if data[0]=='H':
            do_history(c,db,data)



#网络连接
def main():
    #创建数据库连接对象
    db=Database()
    #创建Tcp套接字
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    #循环等待客户端连接
    print("Listen the prot %s"%PORT)
    while True:
        try:
            c,addr=s.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
        #创建子进程
        p=Process(target=do_request,args=(c,db))
        p.daemon=True
        p.start()


if __name__ == "__main__":
    main()


