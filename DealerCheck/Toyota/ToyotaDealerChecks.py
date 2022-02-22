from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import json
import pandas as pd
import csv
import pyautogui as py

def capt(str_inp):
    global json_data
    ms=py.screenshot()
    path=json_data["ss_folder"].strip()+str_inp+".jpeg"
    ms.save(path)


def Error_log(state,city,dealer,reason,url):
    global json_data
    with open(json_data['error_csv_file_name'], 'a') as f:
        writer = csv.writer(f)
        writer.writerow([state, city, dealer, reason,  url])
        ss_name = state + " " + city + " " + dealer
        capt(ss_name)

def Site_run(state, city):
    global df,json_data,driver
    print('In Site_run')
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
        for i in hg: dealer_list.append(i)

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

def tr():
    global json_data,df
    try:
        f = open('ToyotaSettings.json')
        json_data = json.load(f)
        f.close()
    except:
        print('Issue with ToyotaSettings.json File. Make sure it is in the same directory.')

def start():
    global json_data,driver,df
    try:tr()
    except:print("Error with the ToyotaSettings.json file")
    try:
        error_count=1
        s = Service(json_data['chromedriver_path'])
        chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data['proxy'])
        driver = webdriver.Chrome(service=s, chrome_options=chrome_options)

        error_count=2
        driver.get(json_data['url'])
        driver.maximize_window()
        time.sleep(10)
        cur = driver.find_element(By.ID, "btnDealerLocator")
        cur.click()

        error_count=3
        cols=['State','City',"Dealer"]
        df=pd.read_csv(json_data["dealer_csv_name"],usecols=cols)
        with open(json_data['dealer_csv_name'],'r') as r:
            reader=csv.reader(r)
            next(reader)
            for i in reader:Site_run(i[0],i[1])

    except Exception as err:
        print("init",err)
        if error_count==1: print('Error with chromedriver')
        elif error_count==2: print('Error with url')
        elif error_count==3: print('Error with running script')

    finally:
        time.sleep(10)
        driver.close()
        driver.quit()
start()
