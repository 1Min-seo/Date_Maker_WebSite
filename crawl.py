from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time 
from bs4 import BeautifulSoup

chromedriver='C:/Users/python/Webdriver/chromedriver.exe' 
driver = webdriver.Chrome(chromedriver)

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
            print(name.find('span',class_='title').string)  
            print(name.find('span',class_='small-text text-dot-d').string, end='\n\n')
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
            print(name.find('span',class_='title').string)  
            print(name.find('span',class_='small-text text-dot-d').string, end='\n\n')
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
            print(name.find('span',class_='title').string)  
            print(name.find('span',class_='small-text text-dot-d').string, end='\n\n')
        cnt+=1 
        





tourist_attraction()
print('------------------첫 번째 크롤링이 끝났습니다-----------------------')
time.sleep(3) 
entertainment()
print('------------------두 번째 크롤링이 끝났습니다-----------------------')
time.sleep(3)
natural_attraction()
print('------------------세 번째 크롤링이 끝났습니다-----------------------')


 

 
