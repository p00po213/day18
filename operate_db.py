# coding=utf-8
"""
dict项目用于处理数据
"""
import pymysql
import hashlib
import time
class Database:
    def __init__(self,host='192.168.75.128',
                 port=3306,
                 user='root',
                 password='123456',
                 database='dict',
                 charset='utf8'):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database
        self.charset=charset
        self.connect_db() #链接数据库

    def connect_db(self):
        self.db=pymysql.connect(host=self.host,
                                port=self.port,
                                user=self.user,
                                password=self.password,
                                database=self.database,
                                charset=self.charset)
        #这里不创建游标，要在子进程里面处理
    def create_cursor(self):
        self.cur=self.db.cursor()
    #关闭
    def close(self):
        self.cur.close()
        self.db.close()
    def key(self,name,passwd):
        hash=hashlib.md5((name+'the-tang').encode())
        hash.update(passwd.encode())
        return hash.hexdigest()

    #处理注册
    def register(self,name,passwd):
        sql="select * from user where name = '%s';"%name
        self.cur.execute(sql)
        r=self.cur.fetchone()

        if r:
            return False
        sql = "insert into user (name,passwd) values (%s,%s);"

        try:
            self.cur.execute(sql,[name,self.key(name,passwd)])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    #处理登陆
    def login(self,name,passwd):
        sql="select * from user where name='%s';"%name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            if self.key(name,passwd)==r[2]:
                return True
            return False
        else:
            return False
     #插入历史记录
    def insert_history(self,name,word):
        tm=time.ctime()
        sql="insert into hist (name,word,time) values (%s,%s,%s);"
        try:
            self.cur.execute(sql,[name,word,tm])
            self.db.commit()
        except Exception:
            self.db.rollback()
     #查单词
    def query(self,word):
        sql = "select * from words where word='%s'"%word
        self.cur.execute(sql)
        r=self.cur.fetchone()
        if r:
            return r[2]

    def search_history(self,name):
        sql ="select * from hist where name='%s'order by id desc limit 10"%name
        self.cur.execute(sql)
        result=self.cur.fetchall()
        if not result:
            return False
        return result





