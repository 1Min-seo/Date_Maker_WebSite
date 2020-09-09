from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time 
from bs4 import BeautifulSoup 
from  pprint  import pprint
import re




def motel(info) :
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")
    chromedriver='C:/Users/python/Webdriver/chromedriver.exe' 
    driver = webdriver.Chrome(chromedriver ,chrome_options=options)
    driver.get('https://www.yanolja.com/')
    driver.set_window_size(1700,1200) 
    assert "yanolja" in driver.current_url


      
    motel = driver.find_element_by_css_selector('#__next > div.f1e5lflt._2py_lf > nav > div:nth-child(1) > a:nth-child(1) > img')
    motel.click()
    time.sleep(1)
    seoul = driver.find_element_by_css_selector('main div ul li a')
    seoul.click() 
    time.sleep(1)
    area = driver.find_elements_by_xpath("//div[@class='__ZRYy']/a") 
    for location in area : 
        try :
            if info in location.text :
                location.click()
                time.sleep(2)
        except : 
            pass  

    res = driver.page_source
    soup = BeautifulSoup(res,'html.parser')
    
    #가져온 html 소스
    source = soup.select('section._3z8lTy div div div a')
    big_list = [] 
     
    for info in source :
        small_list =[] 
        
        #[이름,링크,이미지,대실시간,대실가격,숙박시간,숙박가격]
        link = 'https://www.yanolja.com'+str(info['href'])
        name = info.select('div div._3bSh4H')[0].string
        a = info.select('div._2TtUOE')[0].find_all('div')[1]
        b = a['style'] 
        items = re.findall('\(([^)]+)',  b)
        img = items[0].strip('""')
        k = soup.select('div span._3UmwxR')
        l = soup.select('div span._2B_pT1') 
        dt = l[0].text 
        dp = k[0].text
        st = l[1].text
        sp = k[1].text
        small_list.append(name)
        small_list.append(link)
        small_list.append(img)
        small_list.append(dt)
        small_list.append(dp)
        small_list.append(st)
        small_list.append(sp)
         
        big_list.append(small_list)


    print(big_list)
    #big_list => list in list 형태 [[],[],[]...]
    return big_list 

#motel('영등포/여의도')

def hotel(info): 
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")
    chromedriver='C:/Users/python/Webdriver/chromedriver.exe' 
    driver = webdriver.Chrome(chromedriver ,chrome_options=options)
    driver.get('https://www.yanolja.com/hotel') 
    driver.set_window_size(1700,1200) 
    assert "yanolja" in driver.current_url
    info = '여의도'
    driver.find_element_by_css_selector('#__next > div:nth-child(1) > div.f1e5lflt.gqhaWX > main > nav > header > a').click() 
    time.sleep(1)
    driver.find_element_by_css_selector('body > div.ReactModalPortal > div > div > section._1BUgxW > div.scroll-content > div > ul > li:nth-child(2) > a').click()
    time.sleep(0.5)
    locations = driver.find_elements_by_css_selector('div  ul  li._2W2P-K  div a')
    for location in locations :
        try : 
            if location.text in info :
                location.click() 
                time.sleep(1)
        except:
            pass 


    res = driver.page_source
    soup = BeautifulSoup(res,'html.parser')
    #가져온 html 소스 

    source = soup.select('div.f1e5lflt._2ECkPU section._3z8lTy div div div a')

    big_list = [] 
    for info in source:
        small_list = [] 
        name = info.select('a div div div._3bSh4H')[0].string 
        link = 'https://www.yanolja.com'+str(info['href']) 
        star = info.select('a div div div._3NpVcW')[0].string
        a = soup.select('div._2TtUOE')[0].find_all('div')[1]
        b = a['style'] 
        items = re.findall('\(([^)]+)',  b)    
        img = items[0].strip('""') 
        price = info.select('div > div > div._2-Y1Xe > span._3UmwxR')[0].string 
        small_list.append(name)
        small_list.append(link)
        small_list.append(star)
        small_list.append(price)
        small_list.append(img) 
        big_list.append(small_list)

    print(big_list)
    return big_list 

hotel('여의도')
       

    



 