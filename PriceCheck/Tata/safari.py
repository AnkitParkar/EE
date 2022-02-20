import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
from PriceCheck.Tata.TataPriceCheck import Error_log

def safari_csv_access(type,model):
    global temp_df,driver,json_data

    car=temp_df.loc[(temp_df['Type']==type)& (temp_df['Variant']==model)]
    bookPrice=car['Booking Price'].to_string(index=False)

    i=1
    while(True):
        try:
            time.sleep(1)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
            xpath = "/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul/li[" + str(i) + "]/div"
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(2)
            xpath="/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul/li["+str(i)+"]/div/p"
            cur = driver.find_element(By.XPATH,xpath)
            print(f'Model {cur.text} done')
            i += 1

        except:
            return

        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[2]/div/div/div[1]/ul/li[3]")  # Get footer booking amount
        bp=''.join([i for i in cur.text if i .isdigit()])
        if bp!=bookPrice: Error_log("Safari",model,type,"Booking Price",bp,bookPrice,driver.current_url)

        time.sleep(2)
        cur = driver.find_element(By.XPATH, "/html/body/app-root/div/app-variants/div[2]/div/div/div[1]/ul/li[3]")# Checkout booking amount
        temp=cur.text
        bp = ''.join([i for i in temp if i .isdigit()])
        if bp!=bookPrice:Error_log("Safari",model,type,"Booking Price",bp,bookPrice,driver.current_url)

        time.sleep(1)
        cur = driver.find_element(By.CLASS_NAME, "chk_btn")#Click on checkout page
        cur.click()

        time.sleep(1)
        cur = driver.find_element(By.CLASS_NAME, "billing-price")#Get prices from checkout page
        bp = ''.join([i for i in cur.text if i .isdigit()])
        if bp!=bookPrice:Error_log("Safari",model,type,"Booking Price",bp,bookPrice,driver.current_url)

        time.sleep(2)
        #print("Safari ",model," ",type," PASSED")
        driver.back()
        time.sleep(4)
    driver.back()

def safari_price_check():
    global temp_df,json_data,driver
    driver.get(json_data['safari_url'])
    driver.maximize_window()


    try:
        #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(4)
        temp_df=df.loc[df['Car']=='safari']
        car_list = ["XZA+ Dark 7S","XZA+ Dark 6S","XTA+ Dark 7S","XZA+ Gold 6S", "XZA+ Gold 7S", "XZA+ 7S", "XZA+ 6S", "XZA 7S", "XMA 7S","XTA+ 7S","XZA+ Adventure 6S", "XZA+ Adventure 7S"]
        for i in range(1, len(car_list)+1):
            print(f'Safari {car_list[i - 1]} automatic')
            xpath_url = "/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[2]/div[2]/div/ul/li[" + str(i) + "]"
            if i >= 6:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(1)
            else:
                driver.execute_script("window.scrollTo(0,0)")
                time.sleep(2)
            time.sleep(3)
            driver.find_element(By.XPATH, xpath_url).click()
            time.sleep(3)
            safari_csv_access("automatic", car_list[i - 1])

        #Selecting Manual
        time.sleep(4)
        driver.execute_script("window.scrollTo(0,0)")
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[1]/div/div/div[1]/div/div[2]/ul/li[2]/label").click()#Selecting manual
        time.sleep(4)

        car_list=["XT+ Dark 7S","XZ+ Dark 7S","XZ+ Dark 6S","XZ+ Gold 6S","XZ+ Gold 7S","XZ+ Adventure 7S","XZ+ Adventure 6S","XZ+ 6S","XZ+ 7S","XZ 7S","XT+ 7S","XT 7S","XM 7S","XE 7S"]
        for i in range(1, len(car_list)+1):
            print(f'Safari {car_list[i-1]} manual')
            xpath_url = "/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[2]/div[2]/div/ul/li[" + str(i) + "]"
            #print(xpath_url)
            if i >= 6:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(1)
            else:
                driver.execute_script("window.scrollTo(0,0)")
            driver.find_element(By.XPATH, xpath_url).click()
            time.sleep(3)
            safari_csv_access("manual", car_list[i - 1])

    except Exception as err:
        print(err)

def safari_start():
    global json_data, df, driver

    f = open('D:/EE/PriceCheck/Tata/TataSettings.json')
    json_data = json.load(f)
    f.close()

    cols = ["Car", "Type", "Variant", "Booking Price", "Showroom Price", "Acc"]
    df = pd.read_csv(json_data["prices_csv_path"], usecols=cols)
    temp_df = pd.DataFrame()
    s = Service(json_data["service_path"])
    chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data["proxy"])
    driver = webdriver.Chrome(service=s, chrome_options=chrome_options)

    safari_price_check()
    driver.close()
    driver.quit()
    print('safari Done')