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
search_keyword = ["Merrill Lynch", "UBS", "Morgan Stanley"]

def data_scrap(link):
    """
    Function to scrap data with search keyword.
    """
    driver.get(link)
    time.sleep(10)
    # Function Call here.
    res = driver.page_source
    soup = BeautifulSoup(res, 'html.parser')
    adviser_name=soup.find('div',{'class':'namesummary flex-noshrink gutter-right layout-wrap ng-binding'})
    # print(adviser_name.text)
    name_list.append(adviser_name.text)
    exp=soup.find_all('div',{'class':'ng-binding dtilecount layout-align-center-stretch'})
    
    securities = soup.find_all('div',{'class': 'sectioncontent'})
  
    location = soup.find_all('a', {'class': 'alink ng-binding ng-scope'})
    link = "https://brokercheck.finra.org"
    for x in location:
       
        firm_list.append(x.text)
        location_list.append(link + x.get('href'))
    for i ,var in  enumerate(location_list):
            driver.get(location_list[i])
            time.sleep(5)
            res = driver.page_source
            soup = BeautifulSoup(res, 'html.parser')
            Address=soup.find_all('div',{'class':"ng-binding"})           
            try:
                street_list.append(Address[3].text)
                city_list.append(Address[4].text.split(",")[0])
                state_zip=(Address[4].text.split(",")[1])
                state_list.append(state_zip.split()[0])
                zip_list.append(state_zip.split()[1])
            except:
                state_list.append("NA")
                state_list.append("NA")
                city_list.append("NA")
                zip_list.append("NA")
    try:
        experince = exp[1].text
        exp_list.append(experince)
    except:
        pass
    try:
        firm = exp[2].text
        firm_list.append(firm)
    except:
        pass

for seaching in search_keyword:
    # Open the chrome driver
    driver = webdriver.Chrome('/home/sunil/workspace/scraping/kelvin/chromedriver_linux64/chromedriver')
    #Hit the url on the chrome driver
    driver.get("https://brokercheck.finra.org")
    # Search keyword
    WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/header/div/div[3]/bc-search/div/md-tabs/md-tabs-content-wrapper/md-tab-content[1]/div/form/div/div[1]/input[1]'))).send_keys(seaching)
    # Search Enter button click.
    driver.find_element_by_xpath('/html/body/div[1]/div/header/div/div[3]/bc-search/div/md-tabs/md-tabs-content-wrapper/md-tab-content[1]/div/form/div/div[1]/input[1]').send_keys(Keys.ENTER)
    time.sleep(4)

    # Html Parser with beautifulSoup.
    res = driver.page_source
    soup = BeautifulSoup(res, 'html.parser')
    # print(soup)
    all_cards=soup.find_all('a',{'class':'md-accent md-raised md-padding md-button ng-scope md-ink-ripple'})
    link = "https://brokercheck.finra.org/"
    for cards in all_cards:
        # card_list.append(cards.text)
        link = "https://brokercheck.finra.org" + cards.get('href')
        data_scrap(link)
    
# This code is for data store in CSV.
c1=pd.Series(data=name_list, name="Advisor Name")

c2=pd.Series(data=firm_list, name="Firm Name")
c3=pd.Series(data=exp_list, name="Years of Experience")
# c4=pd.Series(data=email_list, name="Email Address")
c5=pd.Series(data=street_list, name="Street")

c6=pd.Series(data=city_list, name="city")
c7=pd.Series(data=state_list, name="State")
c8=pd.Series(data=zip_list, name="zip")


data= pd.concat([c1, c2,c3,c5,c6,c7,c8], axis=1)
data_frame=pd.DataFrame(data)
data_frame.to_csv("output.csv")
driver.close()