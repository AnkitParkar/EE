from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import json,csv,time,os
import pyautogui as py
import pandas as pd

def ErrorWrite(car,state,city,dealer_name,reason,url):
    global json_data
    if (os.path.exists(json_data['error_csv_file_name'])) == False:
        em = pd.DataFrame(list())
        em.to_csv('ErrorLogs.csv')
        json_data['error_csv_file_name'] = os.getcwd() + '/ErrorLogs.csv'
        a_file = open('TataSettings.json', "w")
        json.dump(json_data, a_file, indent=2)
        a_file.close()

    with open(json_data["error_csv_file_name"],'a') as f:
        writer=csv.writer(f)
        ss_name = car + state + " " + city + " " + dealer_name
        writer.writerow([car,state,city,dealer_name,reason,ss_name,url])
        capt(ss_name)

def capt(str_inp):
    global json_data
    if os.path.exists(json_data['ss_folder'])==False:
        name='SS_FOLDER'
        os.mkdir(name)
        json_data['ss_folder'] = os.getcwd()+'/SS_FOLDER'
        a_file = open('TataSettings.json', "w")
        json.dump(json_data, a_file, indent=2)
        a_file.close()
    ms=py.screenshot()
    path=json_data["ss_folder"].strip()+'/'+str_inp+".jpeg"
    ms.save(path)

def Site_RunA(car,state,city,dealer_name):
    global json_data,driver
    time.sleep(2)
    try:
        error_type=1
        sel = Select(driver.find_element(By.ID, "state"))
        time.sleep(3)
        sel.select_by_value(state)

        time.sleep(2)
        error_type=2
        sel = Select(driver.find_element(By.ID, "city"))

        time.sleep(3)
        sel.select_by_value(city)

        time.sleep(2)
        error_type=3
        sel = Select(driver.find_element(By.ID, "dealer"))
        time.sleep(4)
        opt = sel.select_by_visible_text(dealer_name)

    except:
        if error_type==1:
            print(" STATE ",state," not present")
            reason="STATE FAIL"
        elif error_type==2:
            print(" CITY ",city," not present in state ",state)
            reason="CITY FAIL"
        elif error_type==3:
            print("DEALER ",dealer_name," not present in city ",city," in state ",state)
            reason="DEALER FAIL"

        ErrorWrite(car, state, city , dealer_name, reason, driver.current_url)

def GetDataA(car):
    global json_data
    time.sleep(5)
    if (os.path.exists(json_data['dealer_csv_name'])==False):
        print('Dealer csv not present or path is wrong')
        return
    with open(json_data["dealer_csv_name"],'r') as f:
        reader=csv.reader(f)
        next(reader)
        for entry in reader:
            state = entry[0].strip()
            city = entry[1].strip()
            dealer_name = entry[2]
            Site_RunA(car,state.upper(),city.upper(),dealer_name)

        print("All entries done")

def Site_RunB(car,state,taluk,dealer_name):
    global json_data,driver
    time.sleep(2)
    try:
        error_type=1
        sel = Select(driver.find_element(By.ID, "state"))
        time.sleep(3)
        sel.select_by_value(state)

        error_type=2
        sel = Select(driver.find_element(By.ID, "taluk"))
        time.sleep(3)
        sel.select_by_value(taluk)

        error_type=3
        sel = Select(driver.find_element(By.ID, "dealer"))
        time.sleep(4)
        sel.select_by_visible_text(dealer_name)

    except:
        if error_type==1:
            print(" STATE ",state," not present")
            reason="STATE FAIL"
        elif error_type==2:
            print(" TALUK ",taluk," not present in state ",state)
            reason="TALUK FAIL"
        elif error_type==3:
            print("DEALER ",dealer_name," not present in taluk ",taluk," in state ",state)
            reason="DEALER FAIL"
        ErrorWrite(car,state,taluk,dealer_name,reason,driver.current_url)

def GetDataB(car):
    global json_data,driver
    time.sleep(5)
    if (os.path.exists(json_data['dealer_csv_name'])==False):
        print('Dealer csv not present or path is wrong')
        return
    driver.refresh()
    time.sleep(3)
    with open(json_data["dealer_csv_name"],'r') as f:
        reader=csv.reader(f)
        next(reader)
        driver.find_element(By.CLASS_NAME, "dealer-info").click()
        for entry in reader:
            state = entry[0]
            taluk = entry[1]
            dealer_name = entry[2]
            Site_RunB(car,state.upper(),taluk.upper(),dealer_name)
        print("All entries done")
    driver.find_element(By.CLASS_NAME, "close-btnm").click()

def tata_dealer_checks_start(car):
    global json_data,driver
    try:
        count = 1
        f = open('TataSettings.json')
        json_data = json.load(f)
        f.close()

        count = 2
        s = Service(json_data['chromedriver_path'])

        count = 3
        chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data['proxy'])
        driver = webdriver.Chrome(service=s, chrome_options=chrome_options)

        count = 4
        print(car)
        driver.get(json_data[car + '_url'])
        driver.maximize_window()
        time.sleep(10)
        if car in ["harrier", "tigor", "tiago"]: GetDataA(car)
        else: GetDataB(car)

    except Exception as err:
        print(err)
        if count==1:
            print('Error with settings file')
        elif count==2:
            print('Error with chromedriver')
        elif count==3:
            print('Error with driver initialistion')
        elif count==4:
            print('Error with site call')
    finally:
        time.sleep(3)
        driver.close()
        driver.quit()
