import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
from PriceCheck.Tata.TataPriceCheck import Error_log

def altroz_csv_access(type,model):
    global temp_df,json_data,driver

    car=temp_df.loc[(temp_df['Type']==type)&(temp_df['Variant']==model)]
    #print(car)
    bookPrice=car['Booking Price'].to_string(index=False)
    showPrice=car['Showroom Price'].to_string(index=False)

    time.sleep(2)
    cur=driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[2]/div/div/div/div[1]/span")#Showroom Price
    temp=cur.text
    sp="".join([i for i in temp if i.isdigit()])
    if sp!=str(showPrice): Error_log("altroz",model,type,"Showroom Price",showPrice,sp,driver.current_url)

    cur=driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[2]/div/div/div/div[2]")#Booking Price
    temp=cur.text
    bp="".join([i for i in temp if i.isdigit()])
    if bp!=str(bookPrice): Error_log("altroz",model,type,"Booking Price",bookPrice,bp,driver.current_url)

    cur = driver.find_element(By.XPATH, "/html/body/app-root/div/app-variants/div[2]/div/div/div[1]/ul/li[3]")# Booking Price
    temp = cur.text
    bp = "".join([i for i in temp if i.isdigit()])
    if bp != str(bookPrice): Error_log("altroz", model, type, "Booking Price", bookPrice, bp, driver.current_url)
    time.sleep(2)

    cur=driver.find_element(By.CLASS_NAME,"chk_btn") #Checkout Button
    cur.click()
    time.sleep(4)
    cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-checkout/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/h3[1]")  #Checkout Showroom Price
    temp = cur.text
    sp = "".join([i for i in temp if i.isdigit()])
    if sp != str(showPrice): Error_log("altroz", model, type, "Showroom Price", showPrice, sp, driver.current_url)

    cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-checkout/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/ul/li/span")  # Checkout Booking Price
    temp = cur.text
    bp = "".join([i for i in temp if i.isdigit()])
    if bp != str(bookPrice): Error_log("altroz", model, type, "Booking Price", bookPrice, bp, driver.current_url)

    cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-checkout/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/div/span")  # Checkout Booking Price
    temp = cur.text
    bp = "".join([i for i in temp if i.isdigit()])
    if bp != str(bookPrice): Error_log("altroz", model, type, "Booking Price", bookPrice, bp, driver.current_url)
    time.sleep(3)
    driver.back()
    time.sleep(3)

def altroz_price_check():
    global temp_df,json_data,df,driver
    try:
        driver.get(json_data['altroz_url'])
        driver.maximize_window()

        temp_df=df.loc[df["Car"]=="altroz"]
    except:
        print("Issue in altroz url or database")

    try:
        time.sleep(4)
        #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        car_list=["XZ+ Dark","XZ+ i-TURBO Dark","XE","XE+","XM+","XT","XT i-TURBO","XZ","XZ i-TURBO","XZ(O)","XZ+","XZ+ i-TURBO"]#Manual list
        for i in range(1,len(car_list)+1):
            if i>6:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(4)
            time.sleep(3)
            temp="/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[2]/div[2]/div/ul/li["+str(i)+"]"
            cur=driver.find_element(By.XPATH,temp)
            cur.click()
            time.sleep(2)
            altroz_csv_access("petrol",car_list[i-1])
            print('altroz',car_list[i-1],"petrol")

        time.sleep(3)
        cur=driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[1]/div/div/div[1]/ul/li[2]/label")
        cur.click()
        time.sleep(3)

        car_list=["XE","XE+","XM+","XT","XZ","XZ(O)","XZ+"]#Automatic List
        for i in range(1,len(car_list)+1):
            if i>6:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(4)
            time.sleep(2)
            temp="/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[2]/div[2]/div/ul/li["+str(i)+"]"
            cur=driver.find_element(By.XPATH,temp)
            cur.click()
            time.sleep(2)
            altroz_csv_access("diesel",car_list[i-1])

    except Exception as err:
        print(err)

def altroz_start():
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

    altroz_price_check()
    driver.close()
    driver.quit()
    print('altroz Done')