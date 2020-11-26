from flask import g
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












