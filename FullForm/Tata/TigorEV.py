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

def csv_access(type,model,variant_xpath,colour):
    global temp_df,driver,json_data

    car=temp_df.loc[(temp_df['Type']==type) & (temp_df['Variant']==model)]
    bookPrice=car['Booking Price'].to_string(index=False).split('.')[0]
    showPrice=car["Showroom Price"].to_string(index=False).split('.')[0]
    i=1
    #print(f'{type} {model} {colour} {bookPrice} {showPrice}')
    xpath='//*[@id="gradient"]/div/div[1]/ul/li[1]'#Name
    cur=driver.find_element(By.XPATH,xpath)
    temp=cur.text.split('\n')[0]
    if temp!=model: Error_log('tigor_ev',model,'ev',colour,'NAME FAIL',None,None,driver.current_url,json_data['error_csv_path'])
    time.sleep(3)

    xpath='//*[@id="gradient"]/div/div[1]/ul/li[2]'#Colour
    cur = driver.find_element(By.XPATH, xpath)
    temp = cur.text.split('\n')[0]
    if temp != colour: Error_log('tigor_ev', model, 'ev', colour, 'COLOUR FAIL', None, None, driver.current_url)
    time.sleep(3)

    xpath='//*[@id="gradient"]/div/div[1]/ul/li[3]'#ShowPrice
    cur = driver.find_element(By.XPATH, xpath)
    temp = ''.join([i for i in cur.text if i.isdigit()])
    if temp != showPrice: Error_log('tigor_ev', model, 'ev', colour, 'SHOWROOM PRICE FAIL',temp,showPrice,driver.current_url)
    time.sleep(3)

    xpath='//*[@id="gradient"]/div/div[2]/div[1]/h3/b'#BookPrice
    cur = driver.find_element(By.XPATH, xpath)
    temp = ''.join([i for i in cur.text if i.isdigit()])
    if temp != bookPrice: Error_log('tigor_ev', model, 'ev', colour, 'BOOKING PRICE FAIL', temp, bookPrice,driver.current_url)
    time.sleep(3)

    driver.find_element(By.XPATH,'//*[@id="gradient"]/div/div[2]/div[2]/div/button').click()#Checkout button
    time.sleep(4)

    xpath='/html/body/app-root/app-checkout/div[2]/form/div/div[1]/div/div/div[1]/div/div/div[2]/span'#Checkout ShowPrice
    cur=''.join([i for i in driver.find_element(By.XPATH,xpath).text if i.isdigit()])
    if showPrice!=cur: Error_log('tigor_ev',model,'ev',colour,'Showroom Price',cur,showPrice,json_data['error_csv_path'])

    xpath = '/html/body/app-root/app-checkout/div[2]/form/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/span'  # Checkout BookPrice 1
    cur = ''.join([i for i in driver.find_element(By.XPATH, xpath).text if i.isdigit()])
    if bookPrice != cur: Error_log('tigor_ev', model, 'ev', colour, 'Booking Price', cur, bookPrice,json_data['error_csv_path'])

    xpath = '/html/body/app-root/app-checkout/div[2]/form/div/div[1]/div/div/div[2]/div[2]/div[2]'  # Checkout BookPrice 2
    cur = ''.join([i for i in driver.find_element(By.XPATH, xpath).text if i.isdigit()])
    if bookPrice != cur: Error_log('tigor_ev', model, 'ev', colour, 'Booking Price', cur, bookPrice,json_data['error_csv_path'])

    temp='Tigor EV '+model
    xpath='/html/body/app-root/app-checkout/div[2]/form/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]'#Model Name
    cur=driver.find_element(By.XPATH,xpath).text.split('(')[0].strip()
    if cur!=temp:Error_log('tigor_ev',model,'ev',colour,'Model name',None,None,driver.current_url,json_data['error_csv_path'])

    xpath='/html/body/app-root/app-checkout/div[2]/form/div/div[1]/div/div/div[2]/div[1]/div[2]/div[1]'#Colour
    cur = driver.find_element(By.XPATH, xpath).text.split('(Sel')[0].strip()
    if cur != colour: Error_log('tigor_ev', model, 'ev', colour, 'Colour name', None, None, driver.current_url,json_data['error_csv_path'])

    cur=driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[1]/div[2]/div[1]')#First Name
    cur.click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[1]/div[2]/div[1]/div/span/input').send_keys('Eccentric')

    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[1]/div[2]/div[2]').click()#Second Name
    time.sleep(2)
    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[1]/div[2]/div[2]/div/span/input').send_keys('Engine')

    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[1]/div[3]').click()#Email
    time.sleep(2)
    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[1]/div[3]/div/span/input').send_keys('eccentric@engine.com')

    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[1]/div[4]/div/ul/li['+str(random.randint(1,2))+']').click()#Parking
    time.sleep(2)

    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[2]/div[1]').click()#Address Line 1
    time.sleep(2)
    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[2]/div[1]/div/span/input').send_keys('ABCD')

    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[2]/div[2]').click()  # Address Line 2
    time.sleep(2)
    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[2]/div[2]/div/span/input').send_keys('EFG')

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)

    # driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[2]/div[3]/div[1]/div').click()#Pincode
    # time.sleep(2)
    # driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[2]/div[3]/div[1]/div/div/span/input').send_keys('400101')
    # time.sleep(3)

    driver.find_element(By.XPATH,'/html/body/app-root/app-checkout/div[2]/form/div/div[2]/div[3]/div[1]/span').click()
    time.sleep(2)
    sel = Select(driver.find_element(By.XPATH, '/html/body/app-root/app-checkout/div[3]/div/form/div[1]/select'))#Select City
    sel.select_by_index(random.randint(1, len(sel.options) - 1))
    time.sleep(2)

    sel = Select(driver.find_element(By.XPATH, '//*[@id="dealer"]'))  # Select Dealer
    sel.select_by_index(random.randint(1, len(sel.options) - 1))
    time.sleep(2)
    driver.find_element(By.CLASS_NAME,'submit-btn').click()
    time.sleep(5)

def select_variant():
    global driver
    car='tigor_ev'
    time.sleep(10)

    variant_xpath='//*[@id="parentVerticalTab"]/ul/li['+str(random.randint(1,4))+']'
    cur=driver.find_element(By.XPATH,variant_xpath)
    cur.click()
    model=cur.text.split('\n')[0]
    time.sleep(3)

    rand=random.randint(1,2)
    xpath='/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[2]/div[2]/ul/li['+str(rand)+']/div/a/span[1]'
    cur=driver.find_element(By.XPATH,xpath)
    cur.click()
    time.sleep(3)
    xpath='/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[2]/div[2]/ul/li['+str(rand)+']/div/div'
    cur=driver.find_element(By.XPATH,xpath)
    colour=cur.text.strip()
    time.sleep(2)
    print(f'{car} : {model} : {colour}')
    csv_access('ev',model,variant_xpath,colour)

def tigor_ev_start():
    global json_data, temp_df, driver
    json_data = dict()
    f = open('D:/EE/FullForm/Tata/TataSettings.json')
    json_data = json.load(f)
    # for i in json_data.keys():
    #   print(i, ":", json_data[i])
    f.close()
    cols = ["Car", "Type", "Variant", "Booking Price", "Showroom Price", "Acc"]
    df = pd.read_csv(json_data["prices_csv_path"], usecols=cols)
    temp_df=df.loc[df['Car']=='tigor_ev']
    s = Service(json_data["service_path"])
    chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data["proxy"])
    driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
    try:
        driver.get(json_data['tigor_ev_url'])
        driver.maximize_window()
        time.sleep(5)
        select_variant()
    except Exception as err:
        print(err)

    finally:
        driver.close()
        driver.quit()
