import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd


global json_data
f = open('D:/EE/PriceCheck/Tata/TataSettings.json')
json_data = json.load(f)
f.close()
s=Service(json_data["service_path"])
chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data["proxy"])
driver=webdriver.Chrome(service=s,chrome_options=chrome_options)

driver.get(json_data['nexon_ev_url'])
driver.maximize_window()

time.sleep(5)
cur=driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[1]/div[3]/div/ul/li[3]")
cur.click()


for i in range(1,9):
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,550)")
    if i>4:
        driver.execute_script("window.scrollTo(0,1000)")
    time.sleep(2)
    temp="/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[3]/div[3]/ul/li["+str(i)+"]/div[2]/div/label"
    cur=driver.find_element(By.XPATH,temp)
    cur.click()
    time.sleep(2)
# time.sleep(4)
# driver.execute_script("window.scrollTo(0,550)")
# time.sleep(2)
#
# cur=driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[3]/div[3]/ul/li[1]/div[2]/div/label")
# cur.click()
# time.sleep(2)
#
# cur = driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[3]/div[3]/ul/li[2]/div[2]/div/label")
# cur.click()
# time.sleep(2)
#
# cur=driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[3]/div[3]/ul/li[3]/div[2]/div/label")
# cur.click()
# time.sleep(3)
#
# cur = driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[3]/div[3]/ul/li[4]/div[2]/div/label")
# cur.click()
# time.sleep(3)
# driver.execute_script("window.scroll(0,1000)")
time.sleep(3)
driver.quit()