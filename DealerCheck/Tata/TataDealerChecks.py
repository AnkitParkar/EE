from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import json,csv,time,os
import pyautogui as py
import pandas as pd

def ErrorWrite(car,state,city,dealer_name,reason,url):
    global json_data,status
    if (os.path.exists(json_data['error_csv_file_name'])) == False:
        em = pd.DataFrame(list())
        em.to_csv('ErrorLogs.csv')
        json_data['error_csv_file_name'] = os.getcwd() + '/ErrorLogs.csv'
        a_file = open('TataSettings.json', "w")
        json.dump(json_data, a_file, indent=2)
        a_file.close()
    status=False
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
    time.sleep(5)
    timeout=10
    #print('In site RunA')
    try:
        error_type=1
        #print('starting')
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(By.ID,'state'))
        driver.find_element(By.ID,'state').click()
        #print('Click done')
        sel = Select(driver.find_element(By.XPATH,'//*[@id="state"]'))
        time.sleep(2)
        sel.select_by_value(state)
        driver.find_element(By.ID, 'state').click()

        time.sleep(2)
        error_type=2
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'city')))
        driver.find_element(By.ID, 'city').click()
        #print('Click done')
        sel = Select(driver.find_element(By.ID, "city"))
        time.sleep(2)
        sel.select_by_value(city)
        driver.find_element(By.ID, 'city').click()

        time.sleep(2)
        error_type=3
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'dealer')))
        driver.find_element(By.ID, 'dealer').click()
        #print('Click done')
        sel = Select(driver.find_element(By.ID, "dealer"))
        time.sleep(2)
        opt = sel.select_by_visible_text(dealer_name)
        driver.find_element(By.ID,'dealer').click()

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
    global json_data,driver,status
    status=True
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'state')))
    if (os.path.exists(json_data['dealer_csv_name'])==False):
        print('Dealer csv not present or path is wrong')
        return
    driver.refresh()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'state')))
    with open(json_data["dealer_csv_name"],'r') as f:
        reader=csv.reader(f)
        next(reader)
        for entry in reader:
            state = entry[0].strip()
            city = entry[1].strip()
            dealer_name = entry[2]
            Site_RunA(car,state.upper(),city.upper(),dealer_name)

        if (os.path.exists(json_data['status_csv_file_name'])) == False:
            em = pd.DataFrame(list())
            em.to_csv('StatusLogs.csv')
            json_data['status_csv_file_name'] = os.getcwd() + '/StatusLogs.csv'
            a_file = open('TataSettings.json', "w")
            json.dump(json_data, a_file, indent=2)
            a_file.close()

        if status:
            with open(json_data['status_csv_file_name'], 'a') as f:
                writer = csv.writer(f)
                writer.writerow([car, 'Passed without issues'])
        else:
            with open(json_data['status_csv_file_name'], 'a') as f:
                writer = csv.writer(f)
                writer.writerow([car, 'Issues, logged in error csv'])
        print("All ",car," entries done")

def Site_RunB(car,state,taluk,dealer_name):
    global json_data,driver
    time.sleep(2)
    try:
        error_type=0
        time.sleep(2)

        error_type=1
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'state')))
        driver.find_element(By.ID, 'state').click()
        sel = Select(driver.find_element(By.ID, "state"))
        time.sleep(2)
        sel.select_by_value(state)
        time.sleep(2)

        error_type=2
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'taluk')))
        driver.find_element(By.ID, 'taluk').click()
        sel = Select(driver.find_element(By.ID, "taluk"))
        time.sleep(2)
        sel.select_by_value(taluk)

        error_type=3

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'dealer')))
        driver.find_element(By.ID, 'dealer').click()
        sel = Select(driver.find_element(By.ID, "dealer"))
        time.sleep(2)
        sel.select_by_visible_text(dealer_name)

        # time.sleep()
        # driver.find_element(By.XPATH,'/html/body/app-root/div/app-checkout/div[1]/div/div/div/form/div[4]/button').click()

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
    global json_data,driver,status
    status=True
    time.sleep(5)
    if car=='safari':
        driver.find_element(By.XPATH,'/html/body/app-root/div/app-variants/div[2]/div/div/div[2]').click()
        time.sleep(2)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'dealer-info')))
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
        if (os.path.exists(json_data['status_csv_file_name'])) == False:
            em = pd.DataFrame(list())
            em.to_csv('StatusLogs.csv')
            json_data['status_csv_file_name'] = os.getcwd() + '/StatusLogs.csv'
            a_file = open('TataSettings.json', "w")
            json.dump(json_data, a_file, indent=2)
            a_file.close()

        if status:
            with open(json_data['status_csv_file_name'], 'a') as f:
                writer = csv.writer(f)
                writer.writerow([car, 'Passed without issues'])
        else:
            with open(json_data['status_csv_file_name'], 'a') as f:
                writer = csv.writer(f)
                writer.writerow([car, 'Issues, logged in error csv'])
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
            print('Error with site call, username password might not have been entered')
    finally:
        time.sleep(3)
        driver.close()
        driver.quit()
