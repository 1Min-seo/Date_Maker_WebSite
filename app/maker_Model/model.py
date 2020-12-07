from flask import g
import json 
import datetime
import re
import time 

class Restaurant:

    @classmethod
    def getRestaurant(cls):
        cursor = g.db.cursor()
        sql ="""SELECT * FROM date_restaurant"""
        cursor.execute(sql)
        data = list(cursor.fetchall()) #튜플 => 리스트
        return data 


class RoomInfo :

    @classmethod
    def getRooms(cls,location):
        cursor = g.db.cursor()
        kind ="호텔"
        try :
            sql = """SELECT room_link,room_img,room_name,room_rate,rate_count,room_price FROM room_table WHERE (room_location='%s') and (room_kind='%s') """ % (location,kind)
            cursor.execute(sql) 
        except :
            print("가져옴 오류")
        data = list(cursor.fetchall())  
        return data 

class PlaceInfo:

    @classmethod
    def getPlace(cls,location):
        cursor = g.db.cursor()
        sql = "select place_location,place_link,place_img,place_name,place_des from place_table WHERE (place_location='%s');" % (location)
        cursor.execute(sql) 
        data = list(cursor.fetchall())
        return data 


class Profile:

    @staticmethod
    def findProfile(user_id):  #프로필이 있는지 없는지 Boolean 으로 
        cursor =  g.db.cursor()
        sql = """select * from date_table where user_id='%s'""" % str(user_id) 
        cursor.execute(sql) 
        profile = cursor.fetchone() 
        if profile :
            return False #있으면 false 
        else:
            return True #없으면 True 
    @classmethod
    def startProfile(cls,user_id,start_day):
        isProfile = cls.findProfile(user_id) # User. 
        if isProfile == False :
            print("이미 프로필이 있는 유저입니다.")
            return False  # 이미 프로필이 생성된 유저 
        cursor = g.db.cursor()   
        day = start_day.split('/')
        year = int(day[0])
        month = int(day[1])
        day = int(day[2])
        meetDay = "%d/%d/%d" % (year,month,day)  #만난 날짜 입력받게 해서 백엔드로 가져온다.
        dayArray= [0,0,0,0,0,0,0] #초기 설정 
        json_dayArray = json.dumps(dayArray,ensure_ascii=False)  
        sql ="""insert into date_table values('%s','%s','%s') """ % (str(meetDay),str(user_id),json_dayArray)
        cursor.execute(sql)
        g.db.commit() 
        return True 
    @staticmethod
    def deleteProfile(user_id):
        try :
            sql ="""DELETE FROM date_table WHERE user_id='%s'""" % user_id
            cursor.execute(sql)
            db.commit()
            print("삭제 완료")
            db.commit()  
            return True
        except : 
            print("없는 유저입니다.")
            return False

    @staticmethod
    def updateDay(user_id,newArray):
        cursor = g.db.cursor()  
        print("갱신 완료")
        json_dayArray = json.dumps(newArray,ensure_ascii=False) 
        sql ="""UPDATE date_table SET date_day='%s' where user_id='%s'""" %  (json_dayArray,str(user_id)) 
        cursor.execute(sql) 
        g.db.commit() 

    @staticmethod
    def resetDay(user_id):
        cursor = g.db.cursor()  
        json_dayArray = json.dumps([0,0,0,0,0,0,0],ensure_ascii=False) 
        sql ="""UPDATE date_table SET date_day='%s' where user_id='%s'""" %  (json_dayArray,str(user_id)) 
        cursor.execute(sql) 
        print("초기화 완료")
        g.db.commit()   

    @staticmethod 
    def getDay(user_id):
        cursor = g.db.cursor()  
        try :
            sql = """select date_day from date_table where user_id='%s'""" % str(user_id)
            cursor.execute(sql)
            dayArray = eval(cursor.fetchone()[0]) 
        except Exception as e:  
            print('에러가 발생 했습니다', e) 
        return dayArray 

    @staticmethod
    def getDate(user_id):
        cursor = g.db.cursor()      
        try:
            sql ="""select meet_day from date_table where user_id='%s'""" % str(user_id)
            cursor.execute(sql)
        except Exception as e: 
            print('에러가 발생 했습니다', e)
        date = list(map(int,cursor.fetchone()[0].split('/')))
        meetday = datetime.datetime(date[0],date[1],date[2]) 
        today = datetime.datetime.now() 
        ingday = re.findall('\d+',str(today-meetday))[0]  
        return int(ingday)+1 #사귄 날부터 1일 설정 


class Cart :

    @staticmethod
    def makeCart(user_id):
        cursor = g.db.cursor()
        json_placeArray = json.dumps([],ensure_ascii=False)   
        json_roomArray = json.dumps([],ensure_ascii=False) 
        json_restaurantArray = json.dumps([],ensure_ascii=False) 
        sql ="""INSERT INTO cart_table (user_id,date_place,date_room,date_restaurant) VALUES('%s','%s','%s','%s');""" % (str(user_id),json_placeArray,json_roomArray,json_restaurantArray)
        cursor.execute(sql) 
        g.db.commit() 
        return True 

    @staticmethod
    def search(data_arr,arr):  
        if arr in data_arr:
            print("이미 있는 아이템입니다.") 
            return True #있을 때 
        else :
            return False  #없을 때
        
    @staticmethod    
    def getItem(user_id):
        cursor = g.db.cursor()
        sql = """select date_place,date_room,date_restaurant from cart_table where user_id='%s'""" % user_id 
        cursor.execute(sql)
        result = cursor.fetchone()
        items= eval(result[0])+eval(result[1])+eval(result[2])
        return items
    
    @classmethod 
    def toggleItem(cls,user_id,arr,num,kind): #kind 가 add 면 toggle 에서 삭제를 수행하지 않도록 만들어야 함. 
        cursor = g.db.cursor()

        if num == 0:  # 0 일때는 먹거리 
            query = ''
            cnt = 0 
            contents = arr[2].split('#')[:7]
            for content in contents :
                if cnt > 2 :
                    break
                if content != '':
                    query += content
                    cnt += 1         
            url = 'https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q='+str(query)
            arr = [url,arr[0],query]
            sql = """select date_restaurant from cart_table where user_id='%s'""" % user_id
            cursor.execute(sql) 
            json_data= cursor.fetchone()[0]
            data_arr = json.loads(json_data) 
            exiest = cls.search(data_arr,arr) 
            if exiest and kind == 'del': #존재한다면  
                data_arr.remove(arr)
            elif not exiest and kind == 'add': # 존재하지 않는다면 
                data_arr.append(arr)
            json_foodArray = json.dumps(data_arr,ensure_ascii=False) 
            sql ="""UPDATE cart_table SET date_restaurant='%s' where user_id='%s'""" %  (json_foodArray,str(user_id)) 

        elif num == 1: # 1 일때는 놀곳
            arr = [arr[1],arr[2],arr[3]]
            sql = """select date_place from cart_table where user_id='%s'""" % user_id
            cursor.execute(sql) 
            json_data= cursor.fetchone()[0]
            data_arr = json.loads(json_data) 
            exiest = cls.search(data_arr,arr) 
            if exiest and kind == 'del': #존재한다면  
                data_arr.remove(arr)
            elif not exiest and kind == 'add': # 존재하지 않는다면 
                data_arr.append(arr)
            json_placeArray = json.dumps(data_arr,ensure_ascii=False) 
            sql ="""UPDATE cart_table SET date_place ='%s' where user_id='%s'""" %  (json_placeArray,str(user_id)) 

        elif num == 2:  # 2 일때는 숙소
            arr = [arr[0],arr[1],arr[2]]
            sql = """select date_room from cart_table where user_id='%s'""" % user_id
            cursor.execute(sql) 
            json_data= cursor.fetchone()[0]
            data_arr = json.loads(json_data) 
            exiest = cls.search(data_arr,arr) 
            if exiest and kind != 'del': #존재한다면  
                data_arr.remove(arr)
            elif not exiest and kind == 'add': # 존재하지 않는다면 
                data_arr.append(arr)
            json_roomArray = json.dumps(data_arr,ensure_ascii=False) 
            sql ="""UPDATE cart_table SET date_room='%s' where user_id='%s'""" %  (json_roomArray,str(user_id)) 
        cursor.execute(sql)    
        g.db.commit() 




    
 











