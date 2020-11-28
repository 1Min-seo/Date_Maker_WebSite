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
from maker_Controller.user_mgmt import User,Login
import os 
from flask import send_from_directory



os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 

app = Flask(__name__,static_url_path='/static')
app.register_blueprint(main_view.pages)
CORS(app) 
app.config.update(
    SECRET_KEY ="woosangyoon1234",
    SESSION_COOKIE_NAME="User_cookie"
)

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

@app.route('/datemaker/main/usercheck',methods=["GET"])
def userCheck():
    response = {
        'name' : "윤우상" 
    }
    return make_response(jsonify(response),200) 

@app.route('/datemaker/seoul/places',methods=["POST","GET"])
def placeRes():
    req = request.get_json()
    print(req)
    location = req['title'] 
    response = PlaceInfo.getPlace(location)
    return make_response(jsonify(response),200) 

if __name__ == "__main__" :
    app.run(debug=1)  



 

    