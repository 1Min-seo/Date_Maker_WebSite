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
from maker_Views import main_view 
from maker_Model.model import Restaurant 
from maker_Model.model import RoomInfo 
from maker_Model.model import PlaceInfo
from maker_Model.model import Profile 
from maker_Controller.user_mgmt import User
import os 
from flask import send_from_directory

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 

app = Flask(__name__,static_url_path='/static')

CORS(app) 
app.config.update(
    SECRET_KEY ="woosangyoon1234",
    SESSION_COOKIE_NAME="User_cookie"
)

app.register_blueprint(main_view.pages)
#모든 유저들을 나타내는 전역변수. User인스턴스 append 하여 관리 
 

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
 
 
@app.before_request
def before_request():
    host_name="localhost"
    host_port = 3306
    user_name = 'root'
    password = 'ywoosang'
    database_name = 'datemaker_db'
    g.db = pymysql.connect(host=host_name,port=host_port,user=user_name,passwd=password,db=database_name,charset='utf8') 
    g.user = None
    if 'user_id' in session:
        user_list = [x for x in User.users if x.id == session['user_id'] ]
        if user_list != [] : 
            g.user = user_list[0]  # user users 에 append 된건 이름,아이디,비번이 넣어진 User 인스턴스임
            print(type(g.user.id))
            print(g.user.id)

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
    def coronaData(cls):  # 지역 별 일일 총 인원/ 일일 증감 
        res = requests.get("https://www.seoul.go.kr/coronaV/coronaStatus.do")
        soup = BeautifulSoup(res.content,"lxml")
        getdata =soup.select("table.tstyle-status.pc.pc-table > tbody")[0] 
        getName = getdata.findAll('th')[:-1] 
        getAdd= getdata.findAll('td',class_="today")[:-1]
        getNum = getdata.findAll('td',class_='')[:-1]
        nameList= list(map(cls.getText,getName))
        numList= list(map(cls.getText,getNum))
        addList= list(map(cls.getText,getAdd))
        return [nameList,numList,addList] #2차원 배열로 만들어준다
    @classmethod
    def seoulData(cls):
        res = requests.get("http://ncov.mohw.go.kr/")
        soup = BeautifulSoup(res.content,"lxml")
        seoulData = soup.select("#map_city1")[0]
        # percent = seoulData.select('div.regional_incidence_ratio > div > div > p')[0].get_text()
        percent = seoulData.find('div',class_="regional_incidence_ratio")['data-percentage']
        getdata = seoulData.select('ul')[0]
        num =getdata.findAll('span',class_ = "num")
        sub_num =getdata.find('span',class_ = "sub_num")
        sub_num=sub_num.string.strip('()')
        numList = deque(list(map(cls.getText,num)))
        numList.appendleft(sub_num)
        numList.appendleft(percent)
        return list(numList)
    @classmethod
    def allData(cls):
        res = requests.get("http://ncov.mohw.go.kr/")
        soup = BeautifulSoup(res.content,"lxml")
        allData = soup.find('div',class_="liveNumOuter")
        content = allData.find_all('span',class_='data')
        domestic = content[0].string
        overseas = content[1].string 
        plus =re.findall('\d+',allData.find('span',class_="before").get_text())[0]
        return [domestic,overseas,plus]


# response API 
@app.route('/datemaker/corona/total',methods=["POST","GET"])
def coronaRes():
    data = {}
    data['coronaData'] = Crawl.coronaData()
    data['seoulData'] = Crawl.seoulData()
    data['allData'] = Crawl.allData()
    response = data
    return make_response(jsonify(response),200) 

@app.route('/datemaker/main/slide/food',methods=["POST"])
def foodimgRes():
    response = Restaurant.getRestaurant()
    return make_response(jsonify(response),200)  

@app.route('/datemaker/restaurant/res',methods=["POST"])
def restaurantRes():
    response = Restaurant.getRestaurant()
    return make_response(jsonify(response),200) 

@app.route('/datemaker/rooms/hotel',methods=["POST","GET"])
def roomsRes():
    req = request.get_json()
    print(req)
    location = req['title'] 
    response = RoomInfo.getRooms(location)
    return make_response(jsonify(response),200) 

@app.route('/datemaker/main/usercheck',methods=["POST"])
def userCheck():
    print("데이터 보내짐")
    if not g.user: 
        name = 'guest'
    else :
        name = str(g.user.name)
    response = {
        'name' : name
    }
    return make_response(jsonify(response),200) 

@app.route('/datemaker/seoul/places',methods=["POST","GET"])
def placeRes():
    req = request.get_json()
    print(req)
    location = req['title'] 
    response = PlaceInfo.getPlace(location)
    return make_response(jsonify(response),200) 


@app.route('/datemaker/profile/makeprofile',methods=["POST","GET"])
def makeProfile():
    req = request.get_json() 
    day = req['day']
    user_id = g.user.id
    print(g.user.id)
    Profile.startProfile(user_id,str(day)) 
    response = jsonify(success=True) 
    date = int(Profile.getDate(str(g.user.id)))
    response = {
        'date' : date
    }
    return make_response(jsonify(response),200) 

@app.route('/datemaker/profile/has',methods=["get","POST"])
def getProfile():
    try :
        user_id = g.user.id
    except : # 세션이 만료된 경우
        return make_response(jsonify('session not found'),402) 
    noProfile = Profile.findProfile(user_id)
    if noProfile :
        response = {
            'profile' : 'no'
        }
    else :
        response = {
            'profile' : 'yes'
        }
    return make_response(jsonify(response),200) 


@app.route('/datemaker/profile/getdate')
def getDay():
    date = int(Profile.getDate(str(g.user.id)))
    response = {
        'date' : date
    }
    return make_response(jsonify(response),200) 


@app.route('/datemaker/profile/getcolors')
def getColors():
    try :
        user_id = g.user.id
    except : # 세션이 만료된 경우
        return abort(402)
    dayArray = Profile.getDay(str(g.user.id))
    response = {
        'colors' : dayArray
    }
    return make_response(jsonify(response),200) 

@app.route('/datemaker/profile/update/date',methods=["POST"])
def getDate():
    print('전송완료')
    req = request.get_json()
    if type(req) == None :
        abort(403)
    print(req)
    print(type(req))
    newArray = req['colors']
    Profile.updateDay(str(g.user.id),newArray)
    response = jsonify(success=True)
    return response
    
@app.route('/datemaker/logout')
def logout():
    session.pop('user_id', None) 
    response = jsonify(success=True) 
    return response

@app.route('/datemaker/profile/renew',methods=["POST"])
def renewDate():
    Profile.resetDay(str(g.user.id))
    response = jsonify(success=True) 
    return response

if __name__ == "__main__" :
    app.run(debug=1)  



 

    