import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
from PriceCheck.Tata.TataPriceCheck import Error_log


def tiago_csv_access(type,model):
    global temp_df,driver,json_data
    i=1
    while(True):
        time.sleep(2)
        try:
            xpath="/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div/div/ul/li["+str(i)+"]"
            cur = driver.find_element(By.XPATH,xpath)  # Colour select
            cur.click()
            time.sleep(2)
            col = driver.find_element(By.XPATH,"/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div[1]/div/h4/span/strong")
            colour=col.text
            #print(f'{colour} {model} done')
            i+=1
        except:
            break
        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div[2]/div[2]/div/button")  # Cost_Select
        temp = cur.text
        price = "".join([i for i in temp if i.isdigit()])
        bp = temp_df.loc[(temp_df['Variant'] == model) & (temp_df['Type'] == type)]
        bookPrice = bp['Booking Price'].to_string(index=False)
        if (price != bookPrice):Error_log("Tiago","Tiago "+model,type,colour,"Booking Price",price,bookPrice,driver.current_url)

    time.sleep(3)

def tiago_price_check():
    global temp_df,json_data,driver,df

    try:driver.get(json_data['tiago_url'])
    except:
        print('Error with tiago url')
        return
    driver.maximize_window()
    time.sleep(10)

    sel = Select(driver.find_element(By.ID, "state"))
    driver.implicitly_wait(10)
    opt = sel.select_by_value("MAHARASHTRA")
    sel = Select(driver.find_element(By.ID, "city"))
    driver.implicitly_wait(10)
    opt = sel.select_by_value("MUMBAI")
    sel = Select(driver.find_element(By.ID, "dealer"))
    driver.implicitly_wait(10)
    opt = sel.select_by_visible_text("Puneet Automobiles-MALAD")

    sel = Select(driver.find_element(By.ID, "fuel"))  # Select Manual
    opt = sel.select_by_value("Petrol-Manual")

    temp_df=df.loc[df['Car']=="tiago"]

    time.sleep(2)
    car_list=["NRG","XE","XT","XZ","XZ+","XZ+DT","XTO"]
    for i in range(1,len(car_list)+1):
        sel=Select(driver.find_element(By.ID,"variant"))
        opt=sel.select_by_index(i)
        time.sleep(2)
        print(f' Tiago manual {car_list[i - 1]} start')
        tiago_csv_access("manual",car_list[i-1])

    sel = Select(driver.find_element(By.ID, "fuel"))  # Select Automatic
    opt = sel.select_by_value("Petrol-Automatic")

    car_list=["NRGA","XZA","XZA+","XZA+DT","XTA"]
    for i in range(1,6):
        sel=Select(driver.find_element(By.ID,"variant"))
        time.sleep(1)
        opt=sel.select_by_index(i)
        time.sleep(2)
        print(f' Tiago automatic {car_list[i-1]} start')
        tiago_csv_access("automatic",car_list[i-1])

    sel = Select(driver.find_element(By.ID, "fuel"))  # Select Automatic
    opt = sel.select_by_value("CNG-Manual")

    try:
        car_list = ["XZ+ CNG", "XZ+ DT CNG","XM CNG","XT CNG"]
        for i in range(1, len(car_list)+1):
            sel = Select(driver.find_element(By.ID, "variant"))
            opt = sel.select_by_index(i)
            time.sleep(2)
            print(f' Tiago cng {car_list[i - 1]} start')
            tiago_csv_access("cng", car_list[i - 1])
    except Exception as err:
        print('Issue in cng',err)

    time.sleep(4)

def tiago_start():
    global json_data,df,driver

    try:
        error_count = 1
        f = open('TataSettings.json')
        json_data = json.load(f)
        f.close()

        error_count = 2
        cols = ["Car", "Type", "Variant", "Booking Price", "Showroom Price", "Acc"]
        df = pd.read_csv(json_data["prices_csv_path"], usecols=cols)
        temp_df = pd.DataFrame()

        error_count = 3
        s = Service(json_data["service_path"])
        chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data["proxy"])
        driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
    except:
        if error_count == 1:
            print('Issue with settings json file')
        elif error_count == 2:
            print('Issue with reading price csv file')
        elif error_count == 3:
            print('Issue with chromedriver initialisation')

    try:
        tiago_price_check()
    finally:
        driver.close()
        driver.quit()
    print('Tiago Done')