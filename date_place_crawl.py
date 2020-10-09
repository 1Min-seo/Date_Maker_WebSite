from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time 
from bs4 import BeautifulSoup 


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR")
chromedriver='C:/Users/python/Webdriver/chromedriver.exe' 
driver = webdriver.Chrome(chromedriver ,chrome_options=options)
driver.get('https://korean.visitseoul.net/index')
driver.set_window_size(1700,1200)
assert "visitseoul" in driver.current_url 

place_name = '강남'

elements = driver.find_elements_by_css_selector('body > div > footer > div.footer-body > div > ul > li:nth-child(4) > ul > li >a')
for name in elements :
    try :
        if name.text == place_name:
            name.click()

    
    except : 
        pass 
  
 
#필요할때 마다 뽑아서 페이지 넘기는 기능을 하게 함. 
 

tourist_dict = {} 
entertainment_dict ={} 
natural_dict = {} 
# 관광명소  
def tourist_attraction(): 
    classified_table= driver.find_elements_by_css_selector('#postSearchFrm > section > div.tag-element > a')
    for name in classified_table :
        try :
            if name.text == '명소':
                name.click() 
        except :
            pass 
    #다음 페이지로 넘어가면 되므로, 
     
    page_nums = driver.find_elements_by_css_selector('#postSearchFrm > section > div.paging-lst > a')
    cnt = 0
    while cnt<=len(page_nums)-1:
        nums = driver.find_elements_by_css_selector('#postSearchFrm > section > div.paging-lst > a')
        if cnt != 0 : 
            nums[cnt].click()
        time.sleep(3)
        res = driver.page_source
        soup = BeautifulSoup(res,'html.parser') 
        names = soup.select('div ul li a div div ') 
        for name in names : 
            title = name.find('span',class_='title').string   
            discription = name.find('span',class_='small-text text-dot-d').string.strip('\t\n')
            tourist_dict[title] = discription 
        cnt+=1  
        
def entertainment():
    classified_table= driver.find_elements_by_css_selector('#postSearchFrm > section > div.tag-element > a')
    for name in classified_table :
        try :
            if name.text == '엔터테인먼트': 
                name.click() 
        except :
            pass
    page_nums = driver.find_elements_by_css_selector('#postSearchFrm > section > div.paging-lst > a')
    cnt = 0
    while cnt<=len(page_nums)-1:
        nums = driver.find_elements_by_css_selector('#postSearchFrm > section > div.paging-lst > a')
        if cnt != 0 : 
            nums[cnt].click()
        time.sleep(3)
        res = driver.page_source
        soup = BeautifulSoup(res,'html.parser') 
        names = soup.select('div ul li a div div ') 
        for name in names :
            title = name.find('span',class_='title').string
            description = name.find('span',class_='small-text text-dot-d').string.strip('\t\n')
            entertainment_dict[title] = description  
        cnt+=1  


def natural_attraction():
    classified_table= driver.find_elements_by_css_selector('#postSearchFrm > section > div.tag-element > a')
    for name in classified_table :
        try :
            if name.text == '자연&관광':
                name.click() 
        except :
            pass
    page_nums = driver.find_elements_by_css_selector('#postSearchFrm > section > div.paging-lst > a')
    cnt = 0
    while cnt<=len(page_nums)-1:
        nums = driver.find_elements_by_css_selector('#postSearchFrm > section > div.paging-lst > a')
        if cnt != 0 : 
            nums[cnt].click()
        time.sleep(3)
        res = driver.page_source
        soup = BeautifulSoup(res,'html.parser') 
        names = soup.select('div ul li a div div ') 
        for name in names :
            title = name.find('span',class_='title').string
            description = name.find('span',class_='small-text text-dot-d').string.strip('\t\n')
            natural_dict[title] = description 
        cnt+=1 
    
tourist_attraction()
time.sleep(3) 
entertainment()
time.sleep(3)
natural_attraction() 

#데이터 베이스에 정보를 집어넣어 프론트에 띄운다. 
import pymysql 
db = pymysql.connect(host='localhost' , port = 3306 , user ='root', 
    passwd='bodu3717@@' ,db='date_maker', charset='utf8') 

cursor= db.cursor()


def insert_database(Dict,cla):
    for title, des in Dict.items() :
        sql =""" INSERT INTO dating_place (TITLE,descript,Classification) VALUES('%s','%s','%s'); """ % (str(title),str(des),str(cla))
        cursor.execute(sql) 


tourist_attraction()
time.sleep(3) 
entertainment()
time.sleep(3)
natural_attraction()  
insert_database(tourist_dict,'명소')
insert_database(entertainment_dict,'엔터테인먼트')
insert_database(natural_dict,'자연&관광') 


