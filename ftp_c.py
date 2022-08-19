from socket import *
import sys
from time import sleep
# 全局变量
HOST='127.0.0.1'
PORT=9000
ADDR=(HOST,PORT)

#具体功能
class FtpClient:
    def __init__(self,sockfd):
        self.sockfd=sockfd

    def do_list(self):
        self.sockfd.send(b'L')  #发送请求
        data=self.sockfd.recv(128).decode()
        if data =='OK':
                data=self.sockfd.recv(4096)
                print(data.decode())
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit('谢谢使用！')
    def do_get(self,filename):
        self.sockfd.send(('G '+filename).encode())
        data=self.sockfd.recv(128).decode()
        if data=='OK':
            #下载文件
            fd=open(filename,'wb')
            while True:
                data=self.sockfd.recv(1024)
                if data ==b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self,filename):
        try:
            fd = open(filename, 'rb')
        except Exception:
            print('没有该文件')
            return
        filename=filename.split("/")[-1]
        self.sockfd.send(('P '+filename).encode())
        data=self.sockfd.recv(128).decode()
        if data=='OK':
            while True:
                data = fd.read(1024)
                if not data:
                    sleep(0.1)
                    print('传送完毕')
                    self.sockfd.send(b'##')
                    fd.close()
                    break
                else:
                    self.sockfd.send(data)
        print(data)









#发起请求
def request(sockfd):

    ftp=FtpClient(sockfd)
    while True:
        print("\n==========命令选项===========")
        print("*********** list ************")
        print("********* get file  *********")
        print("********* put file  *********")
        print("*********** quit ************")
        print("==============================")

        cmd=input("输入命令：")
        if cmd=='list':
            ftp.do_list()
        elif cmd=='quit':
            ftp.do_quit()
        elif cmd[:3]=='get':
            filename=cmd.strip().split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3]=='put':
            filename=cmd.strip().split(' ')[-1]
            ftp.do_put(filename)

#网络连接
def main():
    sockfd=socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        sockfd.connect(ADDR)
    except Exception :
        print("连接服务器失败")
        return
    else:
        print("""
            ************************
             Data   File  Book  Image
            ************************
        """)
        cls=input("请输入文件目录")
        if cls not in ['Data','File','Book','Image']:
            print('Sorry input Error!!')
        else:
            sockfd.send(cls.encode())
            request(sockfd)

if __name__=="__main__":
    main()