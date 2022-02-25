from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time,json,csv,os
import pyautogui as py
import pandas as pd

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
    path=json_data['ss_folder']+str_inp+".jpeg"
    ms.save(path)

def ErrorWrite(car,city,dealer_name,reason,ss_name):
    global json_data,driver
    if (os.path.exists(json_data['error_csv_file_name'])) == False:
        em = pd.DataFrame(list())
        em.to_csv('ErrorLogs.csv')
        json_data['error_csv_file_name'] = os.getcwd() + '/ErrorLogs.csv'
        a_file = open('TataSettings.json', "w")
        json.dump(json_data, a_file, indent=2)
        a_file.close()

    with open(json_data['error_csv_file_name'],'a') as f:
        print("writng")
        writer=csv.writer(f)
        capt(ss_name)
        writer.writerow([car,city,dealer_name,reason,ss_name,driver.current_url])

def Site_Run(car,city,dealer_name):
    global json_data,driver
    count=0
    try:
        error_type=1
        sel = Select(driver.find_element(By.NAME, "city"))
        time.sleep(2)
        sel.select_by_value(city)

        error_type=2
        sel = Select(driver.find_element(By.ID, "dealer"))
        time.sleep(2)
        sel.select_by_visible_text(dealer_name)

    except:
        if error_type==1:
            print(" CITY ",city," not present")
            reason="TALUK FAIL"
        elif error_type==2:
            print("DEALER ",dealer_name," not present in city ",city)
            reason="DEALER FAIL"
        ss_name=car+' '+city+" "+dealer_name.split('-')[0]+reason
        ErrorWrite(car,city,dealer_name,reason,ss_name)

def get_data(car):
    global json_data,driver,status
    status = True
    try:
        if (os.path.exists(json_data['ev_dealer_csv_name']) == False):
            print('EV Dealer csv not present or path is wrong')
            return
        with open(json_data["ev_dealer_csv_name"],'r') as f:
            reader=csv.reader(f)
            next(reader)
            time.sleep(3)
            error_type = 1
            driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[3]/div[1]/span').click()

            for entry in reader:
                city=entry[0].split('-')[1].upper()
                dealer_name = entry[2] + '-' + entry[3].upper()
                #print(city,dealer_name)

                Site_Run(car,city,dealer_name)
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
    except Exception as err:
        print(err,'\n error with Dealer csv ')

    finally:return

def removed_dealers(city, dealer_name):
    try:
        error_type=1
        cur=driver.find_element(By.CLASS_NAME,"dealer-info")
        cur.click()

        error_type = 2
        sel = Select(driver.find_element(By.NAME, "city"))
        time.sleep(2)
        sel.select_by_value(city)

        error_type = 3
        sel = Select(driver.find_element(By.ID, "dealer"))
        time.sleep(2)
        sel.select_by_visible_text(dealer_name)
        error_typE = 4

    except:
        if error_type!=4:
            print("Error with removing dealer ",dealer_name)

    finally:
        return

def ev_dealer_check_start(car):
    global json_data,driver

    try:
        count=1
        f = open('TataSettings.json')
        json_data = json.load(f)
        f.close()

        count=2
        s=Service(json_data['chromedriver_path'])

        count=3
        chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data['proxy'])
        driver = webdriver.Chrome(service=s, chrome_options=chrome_options)

        count=4
        print(car)
        driver.get(json_data[car+'_url'])
        driver.maximize_window()
        time.sleep(15)
        try:driver.find_element(By.XPATH,'//*[@id="gradient"]/div/div[2]/div[2]/div/button').click()#Checkout button tigor
        except:driver.find_element(By.XPATH,'/html/body/app-root/app-variants/div[2]/div/div/div[2]/div[2]/div').click()#Checkout button nexon
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")#Scrolling down on checkout page
        get_data(car)
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

