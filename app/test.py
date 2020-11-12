from flask import Flask,render_template,make_response,jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS 
import json
from collections import deque

app = Flask(__name__,static_url_path='/static')
CORS(app) 
 
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


@app.route('/')
def coronaPage():
    return render_template("public/corona.html") 
     
    
@app.route('/corona',methods=["POST","GET"])
def coronaRes():
    response = Crawl.coronaData() 
    print(response)
    return make_response(jsonify(response),200)





if __name__ == "__main__" :
    app.run(debug=True)
    