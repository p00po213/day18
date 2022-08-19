from socket import *
from threading import Thread
import os,sys
from time import sleep

#全局变量
HOST='127.0.0.1'
PORT=9000
ADDR=(HOST,PORT)
FTP="/home/python/test/day11/ftp/"  #文件库路径

#将客户端请求功能封装为类 L P G Q
class FtpServer:
    def __init__(self,connfd,FTP_PATH):
        self.connfd=connfd
        self.FTP_PATH=FTP_PATH
    def do_list(self):
        #获取文件列表
        files=os.listdir(self.FTP_PATH)
        if not files:
            self.connfd.send("该文件类别为空".encode())
            return
        else:
            self.connfd.send(b'OK')
            sleep(0.1)

        fs=''
        for file in files:
            if file[0]!='.'and os.path.isfile(self.FTP_PATH+file):
                fs+=file + '\n'
        self.connfd.send(fs.encode())
    def do_get(self,filename):
        try:
            fd=open(self.FTP_PATH+filename,'rb')
        except Exception:
            self.connfd.send('文件不存在'.encode())
            return
        else:
            self.connfd.send(b'OK')
            sleep(0.1)
        #发送文件
        while True:
            data=fd.read(1024)
            if not data:
                sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)

    def do_put(self,filename):
        if filename in os.listdir(self.FTP_PATH):
            self.connfd.send("文件已存在".encode())
            return
        self.connfd.send(b'OK')
        print(self.FTP_PATH+filename)
        fd=open(self.FTP_PATH+filename,'wb')
        while True:
            data=self.connfd.recv(1024)
            if data==b'##':
                fd.close()
                break
            fd.write(data)







def handle(connfd):
    cls=connfd.recv(1024).decode()
    FTP_PATH=FTP+cls+'/'
    ftp=FtpServer(connfd,FTP_PATH)
    while True:
        data=connfd.recv(1024).decode()
        if not data or data[0]=='Q':
           return
        elif data[0]=='L':
           ftp.do_list()
        elif data[0]=='G':
            filename=data.split(' ')[-1]
            ftp.do_get(filename)
        elif data[0]=='P':
            filename=data.split(' ')[-1]
            ftp.do_put(filename)




# 网络搭建
def main():
    sockfd=socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("Listen the port %s..."%PORT)
    while True:
        try:
            connfd,addr=sockfd.accept()
        except KeyboardInterrupt:
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        print('连接的客户端：',addr)
    #创建线程处理请求
        client=Thread(target=handle,args=(connfd,))
        client.setDaemon(True)
        client.start()

if __name__=="__main__":
    main()


