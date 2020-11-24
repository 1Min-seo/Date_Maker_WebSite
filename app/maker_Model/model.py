from flask import g
class Restaurant:
    @classmethod
    def getRestaurant(cls):
        cursor = g.db.cursor()
        sql ="""select * from date_restaurant"""
        cursor.execute(sql)
        data = list(cursor.fetchall()) #튜플 => 리스트
        return data 








