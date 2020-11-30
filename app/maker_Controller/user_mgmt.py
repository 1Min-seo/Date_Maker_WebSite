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
    def findProfile(user_id):  #프로필이 있는지 없는지 Boolean 으로 
        cursor = g.db.cursor()
        sql = """select * from date_table where user_id='%s'""" % str(user_id) 
        cursor.execute(sql) 
        profile = cursor.fetchone() 
        if profile :
            return False #있으면 false 
        else:
            return True #없으면 True 

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

    @staticmethod
    def makeProfile(user_id,start_date): #start date = [시작년도,시작월,시작 날] 프론트엔드에서 받아서 입력해주면 백엔드에서 다시 쏴주기 
        userId = user_id  
        isProfile = User.findProfile(userId)
        if isProfile == False :
            return None  # 이미 프로필이 생성된 유저 
        cursor = g.db.cursor() 
        now = time.localtime() 
        year = start_date[0]
        month = start_date[1]
        day = start_date[2]
        meetDay = "%d/%d/%d" % (year,month,day)  #만난 날짜 입력받게 해서 백엔드로 가져온다.
        today = "%04d/%02d/%02d" % (now.tm_year, now.tm_mon, now.tm_mday) #오늘 데이트 했으면 체크할 수 있도록 한다.
        dayArray= [] #초기 설정 
        json_dayArray = json.dumps(dayArray,ensure_ascii=False)  
        sql ="""insert into date_table values('%s','%s','%s') """ % (str(meetDay),str(userId),json_dayArray)
        cursor.execute(sql) 
        g.db.commit() 
        return True # 프로필이 잘 생성된 경우 

    @staticmethod
    def getDate(user_id):
        cursor = g.db.cursor()
        try:
            sql ="""select meet_day from date_table where user_id='%s'""" % str(user_id) 
            cursor.execute(sql)
        except Exception as e: # 에러 종류
            print('에러가 발생 했습니다', e)
        date = list(map(int,cursor.fetchone()[0].split('/')))
        meetday = datetime.datetime(date[0],date[1],date[2]) 
        today = datetime.datetime.now() 
        ingday = re.findall('\d+',str(today-meetday))[0]  
        return int(ingday)+1 #사귄 날부터 1일 설정 

    @staticmethod
    def addDateday(user_id,day):
        cursor = g.db.cursor()
        userId = user_id
        addday = day
        try :
            sql = """select date_day from date_table where user_id='%s'""" % str(userId)
            cursor.execute(sql)
            dayArray = eval(cursor.fetchone()[0]) 
        except Exception as e: # 에러 종류
            print('에러가 발생 했습니다', e)
        if addday not in dayArray: 
            dayArray.append(addday)
            json_dayArray = json.dumps(dayArray,ensure_ascii=False)
            sql ="""UPDATE date_table SET date_day='%s' where user_id='%s'""" %  (json_dayArray,str(userId)) 
            cursor.execute(sql) 
            g.db.commit() 

    @staticmethod
    def delDateday(user_id,day):
        cursor = g.db.cursor()
        delday = day
        try :
            sql = """select date_day from date_table where user_id='%s'""" % str(user_id)
            cursor.execute(sql)
        except Exception as e: # 에러 종류
            print('에러가 발생 했습니다', e)
        dayArray = eval(cursor.fetchone()[0])
        if delday in dayArray: 
            dayArray.remove(delday)
            json_dayArray = json.dumps(dayArray,ensure_ascii=False)
            sql ="""UPDATE date_table SET date_day='%s' where user_id='%s'""" %  (json_dayArray,str(user_id)) 
            cursor.execute(sql) 
            g.db.commit() 