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
    g,
    Blueprint 
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
from maker_Controller.user_mgmt import User 

pages = Blueprint('view',__name__,url_prefix='/')

@pages.route('/')
def gomain():
    return  redirect(url_for('view.main'))

@pages.route('/datemaker')
def main():
    return render_template('public/index.html')


@pages.route('/datemaker/hotel',methods=["GET","POST"])
def hotel():
    return render_template('public/date_hotel.html')

@pages.route('/datemaker/restaurant')
def restaurant():
    return render_template('public/date_restaurant.html')

@pages.route('/datemaker/dateplace')
def dateplace():
    return render_template('public/date_place.html') 

@pages.route('/datemaker/corona')
def coronaPage():
    return render_template("public/corona.html") 

@pages.route('/datemaker/login',methods=["GET","POST"])
def login(): 
    if request.method == "POST":
        session.pop('user_id', None) 
        user_id = request.form.get('Id')
        user_passwd= request.form.get('passwd') 
        user = User.find(user_id) #있는 유저면 user인스턴스 생성
        if user == None or user.passwd != user_passwd:
            makeAlert ="""<script>alert("로그인 오류")</script>""" 
            return render_template("admin/login.html",makeAlert=makeAlert)
        if user.id == user_id and user.passwd == user_passwd:
            session['user_id'] = user.id
            User.users.append(user)
            return redirect(url_for('view.main'))
    return render_template('admin/login.html',makeAlert='') 

@pages.route('/datemaker/signup',methods=["GET","POST"])
def signup(): 
    if request.method == "POST": 
        user_id = request.form.get('Id') 
        user_name = request.form.get('name')
        user_passwd = request.form.get('passwd')
        user = User.makeUser(user_id,user_name,user_passwd)
        if not user : #이미 있는 유저이면 
            makeAlert ="""<script>alert("존재하는 아이디 입니다 ")</script>""" 
            return render_template("admin/sign-up.html",makeAlert=makeAlert)
        return  redirect(url_for('view.login')) 
    return render_template("admin/sign-up.html",makeAlert='')

 

