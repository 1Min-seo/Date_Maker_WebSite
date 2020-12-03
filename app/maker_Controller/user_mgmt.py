from flask import g
import datetime
import time
import re
import json


class User :

    users = []
    def __init__(self,user_id,user_name,user_password):
        self.id = user_id
        self.name =user_name
        self.passwd = user_password
        self.cnt = 0 
    def __repr__(self):
        return f'<Username:{self.name}>' 

    def get_id(self):
        return self.id

    @staticmethod 
    def find(user_id):  # 사용자가 존재하는지 확인
        cursor = g.db.cursor()
        sql = """select * from user_table where user_id='%s'""" % str(user_id) 
        cursor.execute(sql)
        user = cursor.fetchone() #튜플 형식 (아이디,이름,비밀번호)
        if user == None: #없으면 None
            return None
        user_id=user[0]
        user_name=user[1]
        user_passwd=user[2] 
        user = User(user_id,user_name,user_passwd)  #인스턴스 생성
        return user #User 인스턴스가 반환 

   
    @staticmethod
    def makeUser(user_id,user_name,user_passwd):  #회원 가입
        isUser = User.find(user_id) #사용자가 있나 검사 
        if isUser == None :
            cursor = g.db.cursor()
            sql = """insert into user_table (user_id,user_name,user_passwd) values ('%s','%s','%s')""" % (str(user_id),str(user_name),str(user_passwd)) 
            cursor.execute(sql)
            g.db.commit() 
            return True
        else  :
            return False  #이미 있는 유저면 False