
  
from numpy import nanmax, sin
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
search_keyword = [ "UBS","Merrill Lynch"]
# "Merrill Lynch", "UBS", 
driver = webdriver.Chrome('C:\\Users\\DELL\\Downloads\\chromedriver_win32\\chromedriver')

def data_scrap(soup):
    """
    Function to scrap data with search keyword.
    """
    card_conatiner=soup.find('div',{'class':'fullheight'})
    card=card_conatiner.find_all('div',{'class':'flipper'})
    # name=card_conatiner.find_all('span',{'class':'smaller ng-binding flex'})
    for card in card:
        
        single_card=card.find_all('span',{'class':'ng-binding'})
        name_list.append(single_card[0].text)  #adviser name
        print(single_card[0].text)
        try:
            if "PR" in single_card[3].text:
                 firm_list.append("Not Found")    
            else:    
                firm_list.append(single_card[3].text)  # firm_name
        except:
            pass        
        
            
            
        
        try:
            city_list.append(single_card[5].text)    #  city
        except:
            city_list.append("Not Found")
        try:
                state_list.append(single_card[6].text)    #  state
        except:
            state_list.append("Not Found")
        try:
            zip_list.append(single_card[7].text)    #  zip
        except:
            zip_list.append("Not Found")
            
        
            
    exp=card_conatiner.find_all('div',{'class':'md-body-1 flex layout-align-center-center layout-column'})
    for exp in exp:
        if "Y" in exp.text or "N" in exp.text:
            pass
        else:
            exp_list.append(exp.text)
            
        
         
        
   
for seaching in search_keyword:
    # Open the chrome driver
    driver = webdriver.Chrome('C:\\Users\\DELL\\Downloads\\chromedriver_win32\\chromedriver')

  
    driver.get("https://brokercheck.finra.org")
    driver.maximize_window()

        # Search keyword
    WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/header/div/div[3]/bc-search/div/md-tabs/md-tabs-content-wrapper/md-tab-content[1]/div/form/div/div[1]/input[1]'))).send_keys(seaching)
    # Search Enter button click.
    driver.find_element_by_xpath('/html/body/div[1]/div/header/div/div[3]/bc-search/div/md-tabs/md-tabs-content-wrapper/md-tab-content[1]/div/form/div/div[1]/input[1]').send_keys(Keys.ENTER)
    

        # Html Parser with beautifulSoup.
    for i in range(0,1):  
        time.sleep(4)
        res = driver.page_source
        soup = BeautifulSoup(res, 'html.parser')
        time.sleep(5)
        data_scrap(soup)
                    
        try:
            WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div/div/div/section/div[3]/div/div[1]/div/div/div[2]/ul/li[4]'))).click()
        except:
            pass

# # This code is for data store in CSV.
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
