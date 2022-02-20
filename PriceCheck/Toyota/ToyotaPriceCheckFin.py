import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd

#driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

#df=pd.read_csv("ToyotaPriceData.csv",usecols=cols)

def tr():
    global json_data
    f = open('D:/EE/PriceCheck/Toyota/ToyotaSettings.json')
    json_data = json.load(f)
    #for i in json_data.keys():
     #   print(i, ":", json_data[i])
    f.close()


def start():
    global driver,json_data,df,temp_df
    json_data = dict()
    tr()
    cols = ["Car", "Type", "Variant", "Showroom Price", "Price", "Booking Price"]
    df=pd.read_csv(json_data["price_csv_path"],usecols=cols)
    temp_df=pd.DataFrame()
    s=Service(json_data["service_path"])
    chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data["proxy"])
    driver=webdriver.Chrome(service=s,chrome_options=chrome_options)
    try:
        driver.get(json_data['common_site_url'])
        driver.maximize_window()
        time.sleep(5)
        toyota_price_check()

    except:
        print("Back")

    finally:
        driver.quit()

#ZYnd6Enzm6hYjaRc

def Error_log(car_name,model_name,type,colour,price_type,listed_price,actual_price,url):
    print(car_name,model_name,type,price_type,listed_price,actual_price,url,"FAIL")
    with open(json_data['error_csv_path'],'a') as f:
        w=csv.writer(f)
        w.writerow([car_name,model_name,type,colour,price_type,listed_price,actual_price,url])


def toyota_csv_access(car):
    global df,driver,json_data
    car_df=df.loc[df['Car']==car]
    try:
        #temp = car_df.loc[(car_df['Type'] == type) & (car_df['Variant'] == variant)]
        # bp = ''.join([i for i in driver.find_element(By.CLASS_NAME, "tb-registration-cost").text if i.isdigit()])
        # bPrice = car_df['Booking Price'][0].to_string(index=False)
        # print(bp, " : ",bPrice)
        # variant,type=None,None
        # if int(bp) != int(bPrice):
        #     Error_log(car, variant, type, 'default', "Booking Price", bp, bPrice, driver.current_url)
        for i in range(1,car_df.shape[0]+1):
            xpath="//*[@id='divVariantBlock']/div[3]/div/div[1]/ul/li["+str(i)+"]"
            driver.execute_script("window.scrollTo(0,"+str(i*300)+")")
            time.sleep(2)

            cur=driver.find_element(By.XPATH,xpath)
            type=cur.find_element(By.CLASS_NAME,"tb-variants-type").text.lower()+"_"
            type+=cur.find_element(By.CLASS_NAME,"tb-variants-engine").text.lower()
            variant=cur.find_element(By.CLASS_NAME,"tb-variants-title").text

            sp=''.join([i for i in cur.find_element(By.CLASS_NAME,"tb-variants-price").text if i.isdigit()])
            temp = car_df.loc[(car_df['Type'] == type) & (car_df['Variant'] == variant)]
            if i==1:
                bp = ''.join([i for i in driver.find_element(By.CLASS_NAME, "tb-registration-cost").text if i.isdigit()])
                bPrice = temp['Booking Price'].to_string(index=False)
                if int(bp) != int(bPrice):Error_log(car, variant, type, 'default', "Booking Price", bp, bPrice, driver.current_url)
            sPrice=temp['Price'].to_string(index=False)

            if sp!=sPrice: Error_log(car,variant,type,'default',"Showroom Price",sp,sPrice,driver.current_url)
        #"//*[@id='divVariantBlock']/div[3]/div/div[1]/ul/li[2]"
        #print(car_df)
    except Exception as err:
        print("Error in check ",err)

def toyota_price_check():
    driver.execute_script("window.scrollTo(0,0)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,300)")
    time.sleep(2)
    cur = driver.find_element(By.XPATH, "//div[@id='choose-car']/div[1]/div/div/div[1]")
    cur.click()
    time.sleep(3)
    try:
        row,col=1,1
        for i in range(1,8):
            if i > 3:
                driver.execute_script("window.scrollTo(0,800)")
                time.sleep(3)
            elif i==8:
                driver.execute_script("window.scrollTo(0,1400)")
                time.sleep(3)

            xpath="//*[@id='divModelBlock']/div/div/div/div["+str(row)+"]/div["+str(col)+"]"
            cur=driver.find_element(By.XPATH,xpath)
            cur.click()
            time.sleep(3)

            cur=driver.find_element(By.XPATH,"//*[@id='divVariantBlock']/div[2]/div/div")
            car=cur.text
            car=car[car.index('(')+1:car.index(')')].lower()
            toyota_csv_access(car)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0,300)")
            time.sleep(2)
            cur = driver.find_element(By.XPATH, "//div[@id='choose-car']/div[1]/div/div/div[1]")
            cur.click()
            time.sleep(3)

            col+=1
            if col==4:
                row+=1
                col=1

    except Exception as err:
        print(f'{err}')

start()