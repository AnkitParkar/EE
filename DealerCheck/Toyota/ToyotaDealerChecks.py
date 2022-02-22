from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import json
import pandas as pd
import csv

json_data=dict()
s=Service("D:/EE/chromedriver.exe")
PATH= "D:/EE/chromedriver.exe"
PROXY = "11.456.448.110:8080"
chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % PROXY)
driver=webdriver.Chrome(service=s,chrome_options=chrome_options)

def Error_log(state,city,dealer,reason,url):
    with open(json_data['error_csv_file_name'], 'a') as f:
        writer = csv.writer(f)
        writer.writerow([state, city, dealer, reason,  url])

def Site_run(state, city):
    global df
    dealer_df=df.loc[(df['State']==state) & (df['City']==city)]

    try:
        cur_dealer = ''
        error_type=1
        sel = Select(driver.find_element(By.ID, "cboPGSalesState"))
        driver.implicitly_wait(10)
        sel.select_by_visible_text(state.strip())
        opt=sel.first_selected_option
        state=opt.text

        error_type=2
        sel=Select(driver.find_element(By.ID,"cboPGSalesCity"))
        driver.implicitly_wait(10)
        sel.select_by_visible_text(city.strip())
        opt=sel.first_selected_option
        city=opt.text
        time.sleep(5)
        error_type=3

        cur = driver.find_element(By.CLASS_NAME,"tb-accordion")
        temp=cur.text
        hg=temp.split('\n')
        dealer_list=list()
        for i in hg:
            dealer_list.append(i)
        # while(len(dealer_list)>0):
        #     print(state,":",city,":",dealer_list.pop())

        for dealer in dealer_df['Dealer'].tolist():
            if dealer not in dealer_list:
                cur_dealer=dealer
                error_type=3
                raise Exception

    except Exception as err:
        if error_type==1: reason="STATE FAIL"
        elif error_type==2: reason="CITY FAIL"
        elif error_type==3: reason="DEALER FAIL"
        Error_log(state, city, cur_dealer, reason,driver.current_url)


def init_driver():
    global json_data,driver,dealer_df,city_df

    driver.maximize_window()
    driver.get(json_data['url'])
    time.sleep(10)
    cur=driver.find_element(By.ID,"btnDealerLocator")
    cur.click()

def tr():
    global json_data
    f = open('ToyotaSettings.json')
    json_data = json.load(f)
    f.close()


try:
    tr()
    init_driver()
    cols=['State','City',"Dealer"]
    df=pd.read_csv(json_data["dealer_csv_name"],usecols=cols)
    with open(json_data['dealer_csv_name'],'r') as r:
        reader=csv.reader(r)
        next(reader)
        for i in reader:
            Site_run(i[0],i[1])
except Exception as err:
    print("init",err)

finally:
    time.sleep(10)
    driver.close()
