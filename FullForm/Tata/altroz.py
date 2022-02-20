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

def csv_access(type,model,color,bookPrice,showPrice):
    global temp_df,driver

    cur=driver.find_element(By.XPATH,'/html/body/app-root/div/app-variants/div[1]/div[2]/div/div/div/div[1]')#Model check
    if model not in cur.text:Error_log("altroz",model,type,color,"Model Name",None,None,driver.current_url)

    cur=driver.find_element(By.XPATH,'/html/body/app-root/div/app-variants/div[2]/div/div/div[1]/ul/li[1]')#Model check
    if model not in cur.text: Error_log("altroz", model, type,color, "Model Name",None, None, driver.current_url)

    cur=driver.find_element(By.XPATH,'/html/body/app-root/div/app-variants/div[2]/div/div/div[1]/ul/li[2]')#Colour check
    if color not in cur.text: Error_log("altroz", model, type, color,"Colour Name", None, None, driver.current_url)

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

    driver.find_element(By.CLASS_NAME,"chk_btn").click() #Checkout Button
    time.sleep(4)
    mix=model+' ('+type.upper()[0]+') - '+color

    cur=driver.find_element(By.XPATH,'/html/body/app-root/div/app-checkout/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/ul/li')
    temp=cur.text.split('\n')[0]
    if mix!=temp:Error_log("altroz", model, type, "Model Name", None,None, None, driver.current_url)#Checkout model name

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

    cur = driver.find_element(By.XPATH, '//*[@id="firstName"]').click()  # First Name
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="firstName"]').send_keys('Eccentric')

    driver.find_element(By.XPATH, '//*[@id="lastName"]').click()  # Second Name
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="lastName"]').send_keys('Engine')

    driver.find_element(By.XPATH, '//*[@id="email"]').click()  # Email
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="email"]').send_keys('eccentric@engine.com')

    driver.find_element(By.XPATH, '//*[@id="address1"]').click()  # Address Line 1
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="address1"]').send_keys('ABCD')

    driver.find_element(By.XPATH, '//*[@id="address2"]').click()  # Address Line 2
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="address2"]').send_keys('EFG')

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[2]/div[3]/div[1]/div').click()#Pincode
    # time.sleep(2)
    # driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[2]/div[3]/div[1]/div/div/span/input').send_keys('400101')
    # time.sleep(3)

    driver.find_element(By.XPATH, '/html/body/app-root/div/app-checkout/div/div[2]/div/div/div/form/div/div[2]/div/div[3]/div/div/input').click()
    time.sleep(2)

    sel = Select(driver.find_element(By.XPATH, '//*[@id="state"]'))  # Select State
    time.sleep(2)
    sel.select_by_index(random.randint(1, len(sel.options) - 1))
    time.sleep(1)

    sel = Select(driver.find_element(By.XPATH, '//*[@id="taluk"]'))  # Select City
    sel.select_by_index(random.randint(1, len(sel.options) - 1))
    time.sleep(1)

    sel = Select(driver.find_element(By.XPATH, '//*[@id="dealer"]'))  # Select Dealer
    # print(random.randint(1,len(sel.options)-1))
    sel.select_by_index(random.randint(1, len(sel.options) - 1))
    time.sleep(1)

    driver.find_element(By.CLASS_NAME, 'location-btn').click()
    time.sleep(2)
    return

def select_variant(car):
    global driver,json_data

    time.sleep(10)
    xpath='/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[1]/div/div/div[1]/ul/li['+str(random.randint(1,2))+']'
    cur=driver.find_element(By.XPATH,xpath)#Petrol Automatic
    cur.click()
    type=cur.text.lower()
    time.sleep(3)

    cur = driver.find_element(By.XPATH, '//*[@id="parentVerticalTab"]/ul')
    col = cur.find_elements(By.TAG_NAME, 'li')#Variant Select
    #'//*[@id="parentVerticalTab"]/ul/li[1]'
    opt=random.randint(1, len(col))
    if opt >= 6:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(4)
    xpath = '//*[@id="parentVerticalTab"]/ul/li[' + str(opt) + ']'
    #print(xpath)
    col = driver.find_element(By.XPATH, xpath)
    col.click()
    model=col.text
    time.sleep(4)

    # '/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul'
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(4)
    cur = driver.find_element(By.XPATH, '/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul')
    col = cur.find_elements(By.TAG_NAME, 'li')

    # '//*[@id="parentVerticalTab"]/ul/li[1]'
    opt = random.randint(1, len(col) )
    xpath = '/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul/li[' + str(opt) + ']'
    #print(xpath)
    col = driver.find_element(By.XPATH, xpath)
    col.click()
    colour=col.text
    time.sleep(4)
    car_df = df.loc[(df['Type'] == type) & (df['Variant'] == model) & (df['Car']==car)]
    # print(car)
    bookPrice = car_df['Booking Price'].to_string(index=False)
    showPrice = car_df['Showroom Price'].to_string(index=False)
    print(f'{car} : {type} : {model} : {colour} : {bookPrice} : {showPrice}')
    # cur=driver.find_element(By.CLASS_NAME,"chk_btn")
    # cur.click()
    # time.sleep(4)
    csv_access(type,model,colour,bookPrice,showPrice)
    time.sleep(3)

def altroz_start():
    global json_data, df, driver
    json_data = dict()
    f = open('D:/EE/FullForm/Tata/TataSettings.json')
    json_data = json.load(f)
    # for i in json_data.keys():
    #   print(i, ":", json_data[i])
    f.close()
    cols = ["Car", "Type", "Variant", "Booking Price", "Showroom Price", "Acc"]
    df = pd.read_csv(json_data["prices_csv_path"], usecols=cols)
    s = Service(json_data["service_path"])
    chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data["proxy"])
    driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
    try:
        driver.get(json_data['altroz_url'])
        driver.maximize_window()
        time.sleep(5)
        select_variant("altroz")
    except Exception as err:
        print(err)

    finally:
        driver.close()
        driver.quit()

