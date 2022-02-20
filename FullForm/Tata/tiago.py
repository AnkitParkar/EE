from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import random
import pandas as pd
import csv
import json
from FullForm.Tata.ReqMethods import Error_log

def select_dealer():
    global driver,json_data
    car='tiago'
    time.sleep(8)
    try:
        df = pd.read_csv("D:/EE/DealerCheck/Tata/Dealers.csv")
        a = df.sample()
        state, city, dealer, trade = a['State'].to_string(index=False), a['City'].to_string(index=False), a[
            'Trade Name'].to_string(index=False), a['Dealer Name'].to_string(index=False)
    except Exception as err:
        print(f'CSV path issue or CSV issue. {err}')
    try:
        error_type = 1
        sel = Select(driver.find_element(By.ID, "state"))
        driver.implicitly_wait(10)
        opt = sel.select_by_value(state.upper())

        error_type = 2
        sel = Select(driver.find_element(By.ID, "city"))
        driver.implicitly_wait(10)
        opt = sel.select_by_value(city.upper())

        error_type = 3
        sel = Select(driver.find_element(By.ID, "dealer"))
        driver.implicitly_wait(10)
        opt = sel.select_by_visible_text(dealer)
        time.sleep(5)

    except:
        if error_type == 1:
            print(" STATE ", state, " not present")
            reason = "STATE FAIL"
        elif error_type == 2:
            print(" CITY ", city, " not present in state ", state)
            reason = "CITY FAIL"
        elif error_type == 3:
            print("DEALER ", dealer, " not present in city ", city, " in state ", state)
            reason = "DEALER FAIL"
        Error_log('tiago',None,None,None,reason,None,None,driver.current_url,json_data['error_csv_path'])
        return
    time.sleep(4)
    try:
        error_type=1
        sel=Select(driver.find_element(By.XPATH,'//*[@id="fuel"]'))
        #print(random.randint(1,len(sel.options)-1))
        sel.select_by_index(random.randint(1,len(sel.options)-1))
        type=sel.first_selected_option.text
        print(type)
        time.sleep(3)

        error_type=2
        sel = Select(driver.find_element(By.XPATH, '//*[@id="variant"]'))
        # print(random.randint(1,len(sel.options)-1))
        sel.select_by_index(random.randint(1, len(sel.options) - 1))
        variant = sel.first_selected_option.text
        print(variant)
        time.sleep(3)

        error_type=3
        cur=driver.find_element(By.XPATH,'/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div[1]/div/ul')
        col=cur.find_elements(By.TAG_NAME,'li')
        print(len(col))
        xpath='/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div/div/ul/li['+str(random.randint(1, len(col) - 1))+']'
        col=driver.find_element(By.XPATH,xpath)
        col.click()
        time.sleep(4)
    except:
        if error_type == 1:  Error_log(car, None, None, None, 'Car Type Issue', None, None, driver.current_url,json_data['error_csv_path'])
        elif error_type == 2:Error_log(car, type, None, None, 'Car Variant Issue', None, None, driver.current_url,json_data['error_csv_path'])
        elif error_type == 3:Error_log(car, type, variant, None, 'Colour issue', None, None, driver.current_url, json_data['error_csv_path'])

def tiago_start():
    global json_data,driver,df
    json_data = dict()
    f = open('D:/EE/FullForm/Tata/TataSettings.json')
    json_data = json.load(f)
    f.close()
    cols = ["Car", "Type", "Variant", "Booking Price", "Showroom Price", "Acc"]
    df = pd.read_csv(json_data["prices_csv_path"], usecols=cols)
    temp_df = pd.DataFrame()
    s = Service(json_data["service_path"])
    chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data["proxy"])
    driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
    try:
        driver.get(json_data['tiago_url'])
        driver.maximize_window()
        time.sleep(5)
        select_dealer()
    except Exception as err:
        print(err)
    finally:
        driver.close()
        driver.quit()
