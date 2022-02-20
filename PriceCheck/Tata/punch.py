import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
from PriceCheck.Tata.TataPriceCheck import Error_log

def punch_csv_acess(type,model):
    global temp_df,driver,json_data

    i=1
    while(True):
        time.sleep(2)
        try:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            xpath="/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul/li["+str(i)+"]/div/div/a/span[1]"
            driver.find_element(By.XPATH,xpath).click()
            time.sleep(2)
            col=driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul/li[1]/div/p")
            colour=col.text
            #print(f'{colour } {model} done')
            i+=1
        except Exception as err:
            #print(err)
            break

        print("Punch",type,model)
        time.sleep(2)
        car = temp_df.loc[(temp_df['Type'] == type) & (temp_df['Variant'] == model)]
        bookPrice=car['Booking Price'].to_string(index=False)
        showPrice = car["Showroom Price"].to_string(index=False)
        packPrice=car['Acc'].to_string(index=False)
        packPrice=packPrice.split('.')[0]

        #print(f'{bookPrice} : {showPrice} {packPrice}')
        cur=driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[2]/div/div/div/div[2]") #Book Price
        temp=cur.text
        bp="".join([i for i in temp if i.isdigit()])
        if int(bp)!=int(bookPrice): Error_log("punch",model,type, colour,"Booking Price",bookPrice,bp,driver.current_url)

        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[2]/div/div/div[1]/ul/li[3]")  # Book Price
        temp = cur.text
        bp = "".join([i for i in temp if i.isdigit()])
        if int(bp)!=int(bookPrice): Error_log("punch",model,type,colour,"Booking Price",bookPrice,bp,driver.current_url)
        time.sleep(2)

        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[2]/div/div/div/div[1]/span") #Showroom Price
        temp = cur.text
        sp="".join([i for i in temp if i.isdigit()])
        if int(sp)!=int(showPrice): Error_log("punch",model,type,colour,"Showroom Price",showPrice,sp,driver.current_url)
        time.sleep(4)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[3]/div[1]/div/div[1]/div[2]/div/label")  # Pack select
        time.sleep(1)
        cur.click()
        time.sleep(4)
        cur = driver.find_element(By.XPATH, "/html/body/app-root/div/app-variants/div[1]/div[2]/div/div/div/div[1]/span") #Showroom Price
        temp = cur.text
        sp = "".join([i for i in temp if i.isdigit()])
        if int(sp)!=(int(showPrice)+int(packPrice)):Error_log("punch",model,type,colour,"Showroom Price with pack",(int(showPrice)+int(packPrice)),sp,driver.current_url)

        cur = driver.find_element(By.CLASS_NAME, "chk_btn")  # Billing Page
        cur.click()
        time.sleep(3)
        cur=driver.find_element(By.XPATH,"/html/body/app-root/div/app-checkout/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/h3[1]/p") #Checkout Showroom Price
        temp=cur.text
        sp = "".join([i for i in temp if i.isdigit()])
        if int(sp)!=(int(showPrice)+int(packPrice)):Error_log("punch",model,type,colour,"Showroom Price with pack",(int(showPrice)+int(packPrice)),sp,driver.current_url)

        cur=driver.find_element(By.XPATH,"/html/body/app-root/div/app-checkout/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/ul/li/span") #Checkout Book Price
        temp=cur.text
        bp="".join([i for i in temp if i.isdigit()])
        if int(bp)!=int(bookPrice): Error_log("punch",model,type,colour,"Booking Price",bookPrice,bp,driver.current_url)

        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-checkout/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/div/span") #Checkout Book Price
        temp = cur.text
        bp = "".join([i for i in temp if i.isdigit()])
        if int(bp)!=int(bookPrice): Error_log("punch",model,type,colour,"Booking Price",bookPrice,bp,driver.current_url)
        driver.back()
        time.sleep(4)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[3]/div[1]/div/div[1]/div[2]/div/label")  # Pack Deselect
        time.sleep(1)
        cur.click()
        time.sleep(2)

        cur = driver.find_element(By.CLASS_NAME, "chk_btn")  # Billing Page
        cur.click()
        time.sleep(3)

        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-checkout/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/h3[1]/p")  # Checkout Showroom Price
        temp = cur.text
        sp = "".join([i for i in temp if i.isdigit()])
        if int(sp)!=int(showPrice):Error_log("punch",model,type,colour,"Showroom Price",int(showPrice),sp,driver.current_url)
        driver.back()

def punch_price_check():
    global temp_df,driver,json_data,df
    try:
        step=1
        driver.get(json_data['punch_url'])
        driver.maximize_window()

        temp_df=df.loc[df['Car']=='punch']
        time.sleep(10)

        punch_list=["Creative AMT","Accomplish AMT","Adventure AMT"]#Automatic List
        # Automatic Variants
        time.sleep(4)
        for i in range(1,len(punch_list)+1):
            driver.execute_script("window.scrollTo(0,0)")
            temp="/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[2]/div[2]/div/ul/li["+str(i)+"]"
            driver.find_element(By.XPATH,temp).click()
            time.sleep(2)
            punch_csv_acess("automatic",punch_list[i-1])
            time.sleep(4)

        # Select Manual
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,0)")
        driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[1]/div/div/div[1]/ul/li[2]/label").click() # Manual Select
        time.sleep(2)
        punch_list=["Creative","Accomplish","Adventure","Pure"]#Manual List
        for i in range(1,len(punch_list)+1):
            driver.execute_script("window.scrollTo(0,0)")
            temp="/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[2]/div[2]/div/ul/li["+str(i)+"]"
            driver.find_element(By.XPATH,temp).click()
            time.sleep(2)
            punch_csv_acess("manual",punch_list[i-1])
            time.sleep(4)

    except Exception as err:
        print(err)

def punch_start():
    global json_data,df,driver

    f = open('D:/EE/PriceCheck/Tata/TataSettings.json')
    json_data = json.load(f)
    f.close()

    cols = ["Car", "Type", "Variant", "Booking Price", "Showroom Price", "Acc"]
    df = pd.read_csv(json_data["prices_csv_path"], usecols=cols)
    temp_df = pd.DataFrame()
    s = Service(json_data["service_path"])
    chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data["proxy"])
    driver = webdriver.Chrome(service=s, chrome_options=chrome_options)

    punch_price_check()
    driver.close()
    driver.quit()
    print('Punch Done')