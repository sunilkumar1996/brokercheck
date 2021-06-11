from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException, TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import requests
import time
from selenium.webdriver.support.ui import Select
import urllib.request
import pytesseract
from PIL import Image, ImageFilter ,ImageDraw
from pytesseract import pytesseract
import PIL
import urllib.request
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re

name_list = []
exp_list = []
firm_list = []
card_list = []
email_list = []
city_list = []
state_list = []
zip_list = []
street_list = []
location_list = []
link_list=[]
search_keyword = [ "Merrill Lynch", "UBS", "Morgan Stanley"]
# search_keyword = ["UBS"]
# "Merrill Lynch", "UBS", "Morgan Stanley", 

def data_scrap(link):
    """
    Function to scrap data with search keyword.
    """
    driver.get(link)
    time.sleep(10)
    res = driver.page_source
    soup = BeautifulSoup(res, 'html.parser')
    exp=soup.find_all('div',{'class':'ng-binding dtilecount layout-align-center-stretch'})
    try:    
        if "<" in exp[1].text:
            int_exp=(exp[1].text.translate({ord('<'): None}))
        else:
            int_exp=exp[1].text
        
        if int(int_exp) <= 5:
            
            try:
                experince = exp[1].text
                print("expirtgt",experince)
                exp_list.append(experince)
            
            except:
                exp_list.append("N/A")
        
            try:
                adviser_name=soup.find('div',{'class':'smaller font-dark-gray ng-binding ng-scope flex-90'})
                print(adviser_name.text)
                name_list.append(adviser_name.text)
            except:
                pass 
            try:
                firm=soup.find('div',{'class':'bold ng-binding'}) 
                firm_list.append(firm.text)
                print(firm.text,"firm name sssssssssssssssssssssss")
            except:
                firm_list.append("Not found")
                    
            try:
                zip_class = soup.find('div',{'class','employment md-body-1 offset-margintop-1x layout-align-start-start layout-row flex-offset-gt-xs-5 flex-gt-xs-25 flex'})
                zip = zip_class.find_all('span',{'class':'ng-binding'})
                zip_list.append(zip[5].text)
                print(zip[5].text,"ziplist")
            except:
                zip_list.append("Not found")

            try:
                city_list.append(zip[3].text)  
                print(zip[3].text)
            except:
                city_list.append("Not found")

            try:
                state_list.append(zip[4].text)   
            except:
                state_list.append("Not found")          
    except:
            pass

for seaching in search_keyword:
    driver = webdriver.Chrome('/home/sunil/workspace/scraping/kelvin/chromedriver_linux64/chromedriver')
    driver.get("https://brokercheck.finra.org")
    driver.maximize_window()
    WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/header/div/div[3]/bc-search/div/md-tabs/md-tabs-content-wrapper/md-tab-content[1]/div/form/div/div[1]/input[1]'))).send_keys(seaching)
    driver.find_element_by_xpath('/html/body/div[1]/div/header/div/div[3]/bc-search/div/md-tabs/md-tabs-content-wrapper/md-tab-content[1]/div/form/div/div[1]/input[1]').send_keys(Keys.ENTER)
    time.sleep(3)
    res = driver.page_source
    soup = BeautifulSoup(res, 'html.parser')
    pages = soup.find_all('a', {'class': 'ng-binding'})
    page = str(pages[2].text)
    p = page.split(sep=" ", maxsplit=3)
    page_number = int(p[2])
    try:
        for i in range(0, page_number):    
            time.sleep(4)
            res = driver.page_source
            soup = BeautifulSoup(res, 'html.parser')
            all_cards=soup.find_all('a',{'class':'md-accent md-raised md-padding md-button ng-scope md-ink-ripple'})
            experince = soup.find_all('div', {'class': 'row experience layout-row flex-50 ng-scope'})
            link = "https://brokercheck.finra.org/"
            temp_link = []
            for cards in all_cards:
                link = "https://brokercheck.finra.org" + cards.get('href')
                temp_link.append(link)

            temp_exp = []
            for i in experince:
                x = str(i.text)
                obj_split = x.split()
                if "<" in obj_split[3]:
                    last_exp = (obj_split[3].translate({ord('<'): None}))
                else:
                    last_exp = obj_split[3]
                final_exp = int(last_exp)
                temp_exp.append(final_exp)
            
            if temp_link is not None or temp_exp is not None:
                for i in range(0, len(temp_link)):
                    if temp_exp[i] <= 5:
                        link_list.append(temp_link[i])
                        print(temp_link[i])
                    else:
                        pass
                temp_exp.clear()
                temp_link.clear()
            else:
                pass
                
            try:
                WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div/div/div/section/div[3]/div/div[1]/div/div/div[2]/ul/li[4]'))).click()
            except:
                pass
        print(link_list)
        for link in link_list:
            data_scrap(link)          
    except:
        pass


# This code is for data store in CSV.
c1=pd.Series(data=name_list, name="Advisor Name")

c2=pd.Series(data=firm_list, name="Firm Name")
c3=pd.Series(data=exp_list, name="Years of Experience")
# c4=pd.Series(data=email_list, name="Email Address")
# c4=pd.Series(data=street_list, name="Street")

c5=pd.Series(data=city_list, name="city")
c6=pd.Series(data=state_list, name="State")
c7=pd.Series(data=zip_list, name="zip")


data= pd.concat([c1, c2, c3, c5, c6, c7], axis=1)
data_frame=pd.DataFrame(data)
data_frame.to_csv("new.csv")
driver.close()