from flask import Flask,render_template,make_response,jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS 

app = Flask(__name__,static_url_path='/static')
CORS(app)


@app.route('/')
def coronaPage():
    return render_template("public/corona.html")
     
    
@app.route('/corona/res',methods=["POST","GET"])
def coronaRes():
    print("작업 중")
    res = requests.get("https://www.seoul.go.kr/coronaV/coronaStatus.do")
    soup = BeautifulSoup(res.content,"html.parser")
    getName = soup.select("table.tstyle-status.pc.pc-table > tbody > tr:nth-child(1) > th")+soup.select("#move-cont1 > div:nth-child(3) > table.tstyle-status.pc.pc-table > tbody > tr:nth-child(4) > th")
    getNum = soup.select("table.tstyle-status.pc.pc-table > tbody > tr:nth-child(2)>td")+soup.select("#move-cont1 > div:nth-child(3) > table.tstyle-status.pc.pc-table > tbody > tr:nth-child(5) > td")
    nameList=[] 
    numList = []
    coronaDict = {}
    for num in getNum :
        numList.append(num.get_text())
        
    for name in getName:
        nameList.append(name.get_text())
        
    for name,num in zip(nameList[:-1],numList[:-1]): 
        coronaDict[name] = num

    response = coronaDict
    res = make_response(jsonify(response),200)
    return res

    
    
if __name__ == "__main__" :
    app.run(debug=True)
    

