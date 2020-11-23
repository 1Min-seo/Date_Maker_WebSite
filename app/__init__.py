from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    abort, 
    session,
    jsonify,
    make_response,
    g
) 
from flask_cors import CORS 
import json
import requests
from bs4 import BeautifulSoup
from collections import deque
import time
import datetime 
import re
import pymysql 

app = Flask(__name__,static_url_path='/static')
CORS(app) 
app.config.update(
    SECRET_KEY ="woosangyoon1234",
    SESSION_COOKIE_NAME="User_cookie"
)

@app.before_request
def before_request():
    g.db = pymysql.connect(host="localhost", port=3306,user='root',passwd='bodu3717@@',db='user_db',charset='utf8') 
  
@app.teardown_request
def teardown_request(exeption):
    g.db.close()  

class Crawl:
    nameList =[]
    numList =[]
    addList =[]
    @classmethod
    def getText(cls,tag):
        return tag.get_text().strip('+')      
    @classmethod
    def coronaData(cls):
        res = requests.get("https://www.seoul.go.kr/coronaV/coronaStatus.do")
        soup = BeautifulSoup(res.content,"lxml")
        getdata =soup.select("table.tstyle-status.pc.pc-table > tbody")[0] 
        getName = getdata.findAll('th')[:-1] 
        getAdd= getdata.findAll('td',class_="today")[:-1]
        getNum = getdata.findAll('td',class_='')[:-1]
        nameList= list(map(Crawl.getText,getName))
        numList= list(map(Crawl.getText,getNum))
        addList= list(map(Crawl.getText,getAdd))
        return [nameList,numList,addList] #2차원 배열로 만들어준다
    @classmethod
    def seoulData(cls):
        res = requests.get("http://ncov.mohw.go.kr/")
        soup = BeautifulSoup(res.content,"lxml")
        getdata = soup.select("#map_city1 > div > ul")[0]
        num =getdata.findAll('span',class_ = "num")
        sub_num =getdata.find('span',class_ = "sub_num")
        sub_num=sub_num.string.strip('()')
        numList = deque(list(map(Crawl.getText,num)))
        numList.appendleft(sub_num)
        return list(numList)

class Restaurant:
    @classmethod
    def getRestaurant(cls):
        cursor = g.db.cursor()
        sql ="""select * from date_restaurant"""
        cursor.execute(sql)
        data = list(cursor.fetchall()) #튜플 => 리스트
        return data 

class User :
    def __init__(self,user_id,user_name,user_password):
        self.id = user_id
        self.name =user_name
        self.passwd = user_password
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
            return User.find(user_id) #User 인스턴스가 반환
        else  :
            return isUser #User 인스턴스가 반환 

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

 
        
@app.route('/login',methods=["GET","POST"])
def login(): 
    if request.method == "POST":
        cursor = g.db.cursor()
        user_id = request.form.get('Id')
        user_pw = request.form.get('passwd') 
        # name.user = user_id
        try :
            sql = """select id from user_table where id = '%s' """ % user_id
            cursor.execute(sql)
            select_id = cursor.fetchone()
            sql = """SELECT pwd from user_table where pwd = '%s' """ % user_pw
            cursor.execute(sql)
            select_pwd = cursor.fetchone()
            db_id = str(select_id).strip(" ,('')")
            db_pw = str(select_pwd).strip(" ,('')")
            print(db_id)
            print(db_pw) 

        except Exception as e :
            print("예외 발생.", e)
            return redirect(url_for('login',alert="예외 발생")) 

        if user_id == db_id and user_pw == db_pw : 
            #아이디 비번이 일치할 경우 메인페이지로 이동 
            return redirect(url_for('main'))
        else:
            makeAlert ="<script>alert('로그인 오류 !')</script>"  
            return render_template("login.html",makeAlert=makeAlert)  
    return render_template('login.html',makeAlert='')


@app.route('/signup',methods=["GET","POST"])
def signup(): 
    if request.method == "POST":
        cursor = g.db.cursor()
        name = request.form.get('name')
        user_id = request.form.get('Id')
        user_pw = request.form.get('passwd')
        print(name)
        print(user_id)
        print(user_pw)
        # primary key를 id 로 바꿔야 중복이 안됌.
        try : 
            sql ="""insert into user_table values('%s','%s','%s');""" % (str(name),str(user_id),str(user_pw))
            cursor.execute(sql)
        except Exception as e :
            print("예외 발생.", e)
            return redirect(url_for('signup'))  
        sql ="""select * from user_table ;"""
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        g.db.commit()
        #회원가입에 성공한 후 로그인 페이지로 이동 
        return  redirect(url_for('login')) 
    return render_template("sign-up.html")

@app.route('/datemaker/corona')
def coronaPage():
    return render_template("public/corona.html") 
     
@app.route('/corona',methods=["POST","GET"])
def coronaRes():
    response = Crawl.coronaData() 
    print(response)
    return make_response(jsonify(response),200)

@app.route('/')
def gomain():
    return  redirect(url_for('main'))
@app.route('/datemaker')
def main():
    return render_template('public/index.html') 



if __name__ == "__main__" :
    app.run(debug=True)
    