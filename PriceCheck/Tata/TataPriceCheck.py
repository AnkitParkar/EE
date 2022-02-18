import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd

cols=["Car","Type","Variant","Booking Price","Showroom Price"]
df=pd.read_csv("TataDealersPriceData.csv",usecols=cols)
# print(df.keys)
# for i in df:
#     print(i)
# a=df.loc[(df['Car']=='tiago')]
# print(a)
# b=a.loc[(df['Car']=='tiago') & (df['Type']=='manual') & (df['Variant']=='XE')]
# print(b['Booking Price'])
# tigor_manual_list=["XE","XM","XZ","XZ+"]
#
# for variant in tigor_manual_list:
#     b=df.loc[(df['Car']=='tigor')&(df['Type']=='manual')&(df['Variant']==variant)]
#     bp=b['Booking Price'].to_string(index=False)
#     print(bp+":"+variant)
#
# tigor_auto_list=["XMA","XZA+"]
# for variant in tigor_auto_list:
#     b=df.loc[(df['Car']=='tigor')&(df['Type']=='automatic')&(df['Variant']==variant)]
#     print(b['Booking Price'].to_string(index=False)  ," : ",b['Variant'].to_string(index=False))

def Error_log(car_name,model_name,type,colour,price_type,listed_price,actual_price,url):
    print(car_name,model_name,type,price_type,listed_price,actual_price,url,"FAIL")
    with open(json_data['error_csv_path'],'a') as f:
        w=csv.writer(f)
        w.writerow([car_name,model_name,type,colour,price_type,listed_price,actual_price,url])

def tigor_csv_access(type,model):
    global temp_df,driver

    i=1
    while(True):
        try:
            xpath="/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div/div/ul/li["+str(i)+"]"
            cur=driver.find_element(By.XPATH,xpath)
            cur.click()
            time.sleep(2)
            col=driver.find_element(By.XPATH,"/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div[1]/div/h4/span/strong")
            colour=col.text
            print(f'{colour} {model} done')
            i+=1
        except:
            driver.quit()
            break

        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div[2]/div[2]/div/button")  # Cost_Select
        temp = cur.text
        price = "".join([i for i in temp if i.isdigit()])
        bp=temp_df.loc[(temp_df['Variant']==model)&(temp_df['Type']==type)]

        bookPrice=bp['Booking Price'].to_string(index=False)
        if (price != bookPrice):
            print("Error")
            Error_log("Tigor", "Tigor(P) "+model, type, colour, "Booking Price",price, bookPrice, json_data['tigor_url'])

def tigor_price_check():
    global temp_df
    driver.get(json_data['tigor_url'])
    driver.maximize_window()

    sel = Select(driver.find_element(By.ID, "state"))
    driver.implicitly_wait(10)
    opt = sel.select_by_value("MAHARASHTRA")
    sel = Select(driver.find_element(By.ID, "city"))
    driver.implicitly_wait(10)
    opt = sel.select_by_value("MUMBAI")
    sel = Select(driver.find_element(By.ID, "dealer"))
    driver.implicitly_wait(10)
    opt = sel.select_by_visible_text("Puneet Automobiles-MALAD")

    sel = Select(driver.find_element(By.ID,"fuel"))#Select Manual
    opt  = sel.select_by_value("Petrol-Manual")

    time.sleep(2)
    temp_df=df.loc[df['Car']=="tigor"]
    tigor_manual_list=["XE","XM","XZ","XZ+"]
    for i in range(1,5):
        sel = Select(driver.find_element(By.ID,"variant"))
        opt = sel.select_by_index(i)
        time.sleep(2)
        print("Tigor", tigor_manual_list[i-1], " start")
        tigor_csv_access("manual",tigor_manual_list[i-1])

    sel = Select(driver.find_element(By.ID, "fuel"))  # Select Automatic
    opt = sel.select_by_value("Petrol-Automatic")

    tigor_auto_list=["XMA","XZA+"]
    for i in range(1,3):
        sel = Select(driver.find_element(By.ID,"variant"))
        opt = sel.select_by_index(i)
        time.sleep(2)
        print(f'Tigor {tigor_auto_list[i-1]} start')
        tigor_csv_access("automatic",tigor_auto_list[i-1])

    sel = Select(driver.find_element(By.ID, "fuel"))  # Select Automatic
    opt = sel.select_by_value("CNG-Manual")

    tigor_cng_manual_list = ["XZ+ CNG", "XZ CNG"]
    for i in range(1, 3):
        sel = Select(driver.find_element(By.ID, "variant"))
        opt = sel.select_by_index(i)
        time.sleep(2)
        tigor_csv_access("cng", tigor_cng_manual_list[i - 1])

    time.sleep(5)
    driver.quit()

def tiago_csv_access(type,model):
    global temp_df,driver

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
            print(f'{colour} {model} done')
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

    global temp_df
    driver.get(json_data['tiago_url'])
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
    for i in range(1,8):
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

    car_list = ["XZ+ CNG", "XZ+ DT CNG","XM CNG","XT CNG"]
    for i in range(1, 4):
        sel = Select(driver.find_element(By.ID, "variant"))
        opt = sel.select_by_index(i)
        time.sleep(2)
        print(f' Tiago cng {car_list[i - 1]} start')
        tiago_csv_access("cng", car_list[i - 1])

    time.sleep(4)
    driver.close()

def harrier_csv_access(type,model):
    global temp_df,driver

    i=1
    while(True):
        time.sleep(2)
        try:
            xpath = "/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div/div/ul/li[" + str(i) + "]"
            cur = driver.find_element(By.XPATH, xpath)  # Colour select
            cur.click()
            time.sleep(2)
            col = driver.find_element(By.XPATH,"/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div[1]/div/h4/span/strong")
            colour=col.text
            print(f'{colour} {model} done')
            i += 1
        except:
            break

        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/div[2]/app-new-customer/div[2]/div/div[2]/div[2]/div/div/button")  # Cost_Select
        temp = cur.text
        price = "".join([i for i in temp if i.isdigit()])
        bp = temp_df.loc[(temp_df['Variant'] == model) & (temp_df['Type'] == type)]
        bookPrice = bp['Booking Price'].to_string(index=False)
        if (price != bookPrice):Error_log("Harrier", model, type, colour, "Booking Price",price, bookPrice, json_data['harrier_url'])
    time.sleep(3)

def harrier_price_check():
    global temp_df
    url=json_data["harrier_url"]
    driver.get(url)
    driver.maximize_window()

    time.sleep(5)

    sel = Select(driver.find_element(By.ID, "state"))
    driver.implicitly_wait(10)
    opt = sel.select_by_value("MAHARASHTRA")
    sel = Select(driver.find_element(By.ID, "city"))
    driver.implicitly_wait(10)
    opt = sel.select_by_value("MUMBAI")
    sel = Select(driver.find_element(By.ID, "dealer"))
    driver.implicitly_wait(10)
    opt = sel.select_by_visible_text("Puneet Automobiles-MALAD")
    time.sleep(5)

    temp_df=df.loc[df['Car']=="harrier"]
    sel = Select(driver.find_element(By.XPATH,"/html/body/app-root/div/div[2]/app-new-customer/div/div[2]/form/div/div[4]/div/select"))  # Select Manual
    opt = sel.select_by_value("Diesel-Manual")
    time.sleep(2)
    car_list=["XE","XM","XT","XT+","XT+ Dark Edition","XZ","XZ Dual Tone","XZ+","XZ+ Dual Tone"]
    for i in range(1,len(car_list)+1):
        sel=Select(driver.find_element(By.ID,"variant"))
        opt=sel.select_by_index(i)
        time.sleep(2)
        print(f'Harrier {car_list[i-1]} start')
        harrier_csv_access("manual",car_list[i-1])

    sel = Select(driver.find_element(By.XPATH,"/html/body/app-root/div/div[2]/app-new-customer/div/div[2]/form/div/div[4]/div/select"))  # Select Automatic
    opt = sel.select_by_value("Diesel-Automatic")
    time.sleep(2)
    car_list=["XMA","XZA","XZA Dual Tone","XZA+","XZA+ Dual Tone","XTA+"]
    for i in range(1, len(car_list) + 1):
        sel = Select(driver.find_element(By.ID, "variant"))
        opt = sel.select_by_index(i)
        time.sleep(2)
        print(f'Harrier {car_list[i - 1]} start')
        harrier_csv_access("automatic", car_list[i - 1])

    driver.quit()

def altroz_csv_access(type,model):
    global temp_df

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
    global temp_df
    driver.get(json_data['altroz_url'])
    driver.maximize_window()

    temp_df=df.loc[df["Car"]=="altroz"]

    try:
        time.sleep(4)
        #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        car_list=["XZ+ Dark","XZ+ i-TURBO Dark","XE","XE+","XM+","XT","XT i-TURBO","XZ","XZ i-TURBO","XZ(O)","XZ+","XZ+ i-TURBO"]#Manual list
        for i in range(1,len(car_list)+1):
            if i>=6:
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
        for i in range(1,8):
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

def tigor_ev_csv_access(type,model,variant_xpath):
    global temp_df

    #print("Tigor EV",model)
    time.sleep(2)
    car=temp_df.loc[(temp_df['Type']==type) & (temp_df['Variant']==model)]
    bookPrice=car['Booking Price'].to_string(index=False).split('.')[0]
    showPrice=car["Showroom Price"].to_string(index=False).split('.')[0]
    i=1
    while(True):
        try:
            #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            xpath="/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[2]/div[2]/ul/li["+str(i)+"]/div/a/span[1]"
            cur=driver.find_element(By.XPATH,xpath)
            cur.click()
            time.sleep(1)
            xpath="/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[2]/div[2]/ul/li["+str(i)+"]/div/div"
            cur=driver.find_element(By.XPATH,xpath)
            colour=cur.text
            #print(f'{model} {colour} done')
            i+=1
        except:
            break

        dir = driver.find_element(By.CLASS_NAME, "resp-tab-active")
        cur = dir.find_element(By.CLASS_NAME, "priceVariant")
        temp=cur.text.split('\n')[0]
        sp="".join([i for i in temp if i.isdigit()])
        if sp!=showPrice: Error_log("Tigor EV",model,type,colour, "Showroom Price",sp,showPrice,driver.current_url)
        time.sleep(2)

        cur=driver.find_element(By.CLASS_NAME,"activeprice")
        temp = cur.text.split('\n')[0]
        sp = "".join([i for i in temp if i.isdigit()])
        if sp != showPrice: Error_log("Tigor EV", model, type, colour, "Showroom Price", sp, showPrice,driver.current_url)
        time.sleep(2)

        cur=driver.find_element(By.CLASS_NAME,"co-check-title")
        temp = cur.text.split('\n')[0]
        bp = "".join([i for i in temp if i.isdigit()])
        if bp != bookPrice: Error_log("Tigor EV", model, type, colour, "Booking Price",bp, bookPrice,driver.current_url)
        time.sleep(2)

        cur=driver.find_element(By.CLASS_NAME,"chk_btn")
        cur.click()
        time.sleep(2)
        cur=driver.find_element(By.CLASS_NAME,"amnt_r")
        temp = cur.text.split('\n')[0]
        sp = "".join([i for i in temp if i.isdigit()])
        if sp != showPrice: Error_log("Tigor EV", model, type, colour, "Showroom Price",sp, showPrice,driver.current_url)
        time.sleep(2)

        cur=driver.find_element(By.XPATH,"/html/body/app-root/app-checkout/div[2]/form/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]")
        temp = cur.text.split('\n')[0]
        bp = "".join([i for i in temp if i.isdigit()])
        if bp != bookPrice: Error_log("Tigor EV", model, type, colour, "Booking Price",bp, bookPrice,driver.current_url)
        time.sleep(2)

        cur=driver.find_element(By.CLASS_NAME,"total_prc")
        temp = cur.text.split('\n')[0]
        bp = "".join([i for i in temp if i.isdigit()])
        if bp != bookPrice: Error_log("Tigor EV", model, type, colour, "Booking Price",bp, bookPrice,driver.current_url)
        time.sleep(2)
        driver.back()
        time.sleep(2)
        cur=driver.find_element(By.XPATH,variant_xpath)
        cur.click()
        time.sleep(2)

def tigor_ev_price_check():
    global temp_df
    driver.get(json_data['tigor_ev_url'])
    driver.maximize_window()

    temp_df=df[df["Car"]=='tigor_ev']
    car_list=['XZ+ DT','XZ+','XM','XE']
    try:
        for i in range(1,len(car_list)+1):
            time.sleep(3)#First variant
            variant_xpath = "/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[1]/div[3]/div/ul/li["+str(i)+"]"
            cur=driver.find_element(By.XPATH,variant_xpath)
            cur.click()
            time.sleep(2)
            tigor_ev_csv_access("ev",car_list[i-1],variant_xpath)

    except Exception as err:
        print(err)

def nexon_imag_csv_access(type, model):
    global temp_df

    time.sleep(3)
    cur = driver.find_element(By.CLASS_NAME, "new-book-online-btn")
    cur.click()
    time.sleep(4)

    cur=driver.find_element(By.XPATH,"/html/body/app-root/div/app-checkout/div[1]/div[2]/div/div/div/form/div/div[1]/div/div[1]/ul/li/span")
    temp=cur.text
    bp=temp.split(' ')[0]+temp.split(' ')[1]
    print(bp,":",model)
    time.sleep(2)

    cur=driver.find_element(By.XPATH,"/html/body/app-root/div/app-checkout/div[1]/div[2]/div/div/div/form/div/div[1]/div/div[1]/div/span")
    temp = cur.text
    bp=temp.split(' ')[0]+temp.split(' ')[1]
    print(bp,":",model)
    time.sleep(2)
    driver.back()
    time.sleep(4)

def nexon_imag_price_check():
    driver.get(json_data['nexon_imag_url'])
    driver.maximize_window()

    try:
        nexon_imag_list=["Nexon(P)XZ+ Dark","Nexon(D)XZ+ Dark","Nexon(D)XZ+ (O)Dark","Nexon(P)XZ+ (O)Dark"]
        time.sleep(20)
        #"/html/body/div/div/div[4]/div/div/div[1]/div[4]"
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        nexon_imag_csv_access("manual","Nexon(P)XZ+ Dark")
        time.sleep(20)
        cur=driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div/ul/li[2]/label/div[1]")
        cur.click()
        nexon_imag_csv_access("manual","Nexon(D)XZ+ Dark")

        time.sleep(10)
        cur = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div/ul/li[3]/label/div[1]")
        cur.click()
        nexon_imag_csv_access("manual","Nexon(P)XZ+ (O)Dark")

        time.sleep(10)
        cur = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div/ul/li[4]/label/div[1]/div[1]")
        cur.click()
        nexon_imag_csv_access("manual","Nexon(D)XZ+ (O)Dark")

    finally:
        time.sleep(3)
        driver.quit()

def punch_csv_acess(type,model):
    global temp_df,driver

    i=1
    while(True):
        time.sleep(2)
        try:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            xpath="/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul/li["+str(i)+"]/div/div/a/span[1]"
            cur=driver.find_element(By.XPATH,xpath)
            cur.click()
            time.sleep(2)
            col=driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul/li[1]/div/p")
            colour=col.text
            print(f'{colour } {model} done')
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
    global temp_df
    try:
        step=1
        driver.get(json_data['punch_url'])
        driver.maximize_window()

        temp_df=df.loc[df['Car']=='punch']
        time.sleep(10)

        punch_list=["Creative AMT","Accomplish AMT","Adventure AMT"]#Automatic List
        # Automatic Variants
        time.sleep(4)
        for i in range(1,4):
            driver.execute_script("window.scrollTo(0,0)")
            temp="/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[2]/div[2]/div/ul/li["+str(i)+"]"
            cur=driver.find_element(By.XPATH,temp)
            cur.click()
            time.sleep(2)
            punch_csv_acess("automatic",punch_list[i-1])
            time.sleep(4)

        # Select Manual
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,0)")
        cur = driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[1]/div/div/div[1]/ul/li[2]/label") # Manual Select
        cur.click()
        time.sleep(2)
        punch_list=["Creative","Accomplish","Adventure","Pure"]#Manual List
        for i in range(1,5):
            driver.execute_script("window.scrollTo(0,0)")
            temp="/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[2]/div[2]/div/ul/li["+str(i)+"]"
            cur=driver.find_element(By.XPATH,temp)
            cur.click()
            time.sleep(2)
            punch_csv_acess("manual",punch_list[i-1])
            time.sleep(4)

    except Exception as err:
        print("Hoagaya exception bhai ",step)
        print(err)

def safari_csv_access(type,model):
    global temp_df,driver

    car=temp_df.loc[(temp_df['Type']==type)& (temp_df['Variant']==model)]
    bookPrice=car['Booking Price'].to_string(index=False)

    i=1
    while(True):
        try:
            time.sleep(1)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
            xpath = "/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[4]/div[1]/div[1]/ul/li[" + str(i) + "]/div"
            cur = driver.find_element(By.XPATH, xpath)
            cur.click()
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
    driver.get(json_data['safari_url'])
    driver.maximize_window()
    global temp_df

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
            cur = driver.find_element(By.XPATH, xpath_url)
            cur.click()
            time.sleep(3)
            safari_csv_access("automatic", car_list[i - 1])

        #Selecting Manual
        time.sleep(4)
        driver.execute_script("window.scrollTo(0,0)")
        cur=driver.find_element(By.XPATH,"/html/body/app-root/div/app-variants/div[1]/div[1]/form/div[1]/div/div/div[1]/div/div[2]/ul/li[2]/label")#Selecting manual
        cur.click()
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
            cur = driver.find_element(By.XPATH, xpath_url)
            cur.click()
            time.sleep(3)
            safari_csv_access("manual", car_list[i - 1])

    except Exception as err:
        print("Lafda hogaya")
        print(err)

def nexon_ev_price_check():
    driver.get(json_data['nexon_ev_url'])
    driver.maximize_window()

    time.sleep(5)
    cur=driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[1]/div[3]/div/ul/li[3]")
    cur.click()

    time.sleep(4)
    driver.execute_script("window.scrollTo(0,550)")
    time.sleep(2)

    cur=driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[3]/div[3]/ul/li[1]/div[2]/div/label")
    cur.click()
    time.sleep(2)

    cur = driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[3]/div[3]/ul/li[2]/div[2]/div/label")
    cur.click()
    time.sleep(2)

    cur=driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[3]/div[3]/ul/li[3]/div[2]/div/label")
    cur.click()
    time.sleep(3)

    cur = driver.find_element(By.XPATH,"/html/body/app-root/app-variants/div[1]/div[1]/div[2]/form/div[3]/div[3]/ul/li[4]/div[2]/div/label")
    cur.click()
    time.sleep(3)
    driver.execute_script("window.scroll(0,1000)")
    time.sleep(3)
    driver.quit()

def safari_imag_price_check():
    global temp_df
    # driver.get(json_data['tiago_url'])
    # driver.maximize_window()
    # time.sleep(10)
    # sel = Select(driver.find_element(By.ID, "state"))
    # driver.implicitly_wait(10)
    # opt = sel.select_by_value("MAHARASHTRA")
    # sel = Select(driver.find_element(By.ID, "city"))
    # driver.implicitly_wait(10)
    # opt = sel.select_by_value("MUMBAI")
    # sel = Select(driver.find_element(By.ID, "dealer"))
    # driver.implicitly_wait(10)
    # opt = sel.select_by_visible_text("Puneet Automobiles-MALAD")
    #
    # sel = Select(driver.find_element(By.ID, "fuel"))  # Select Manual
    # opt = sel.select_by_value("Petrol-Manual")

    temp_df = df.loc[df['Car'] == "tiago"]
    print(temp_df)
    car_list= list(temp_df.loc[temp_df['Type']=='manual'])
    print(car_list)
    time.sleep(2)
    car_list = ["NRG", "XE", "XT", "XZ", "XZ+", "XZ+DT", "XTO"]
    # for i in range(1, 8):
    #     sel = Select(driver.find_element(By.ID, "variant"))
    #     opt = sel.select_by_index(i)
    #     time.sleep(2)
    #     print(f' Tiago manual {car_list[i - 1]} start')
    #     tiago_csv_access("manual", car_list[i - 1])
    #
    # sel = Select(driver.find_element(By.ID, "fuel"))  # Select Automatic
    # opt = sel.select_by_value("Petrol-Automatic")
    #
    # car_list = ["NRGA", "XZA", "XZA+", "XZA+DT", "XTA"]
    # for i in range(1, 6):
    #     sel = Select(driver.find_element(By.ID, "variant"))
    #     time.sleep(1)
    #     opt = sel.select_by_index(i)
    #     time.sleep(2)
    #     print(f' Tiago automatic {car_list[i - 1]} start')
    #     tiago_csv_access("automatic", car_list[i - 1])
    #
    # sel = Select(driver.find_element(By.ID, "fuel"))  # Select Automatic
    # opt = sel.select_by_value("CNG-Manual")
    #
    # car_list = ["XZ+ CNG", "XZ+ DT CNG", "XM CNG", "XT CNG"]
    # for i in range(1, 4):
    #     sel = Select(driver.find_element(By.ID, "variant"))
    #     opt = sel.select_by_index(i)
    #     time.sleep(2)
    #     print(f' Tiago cng {car_list[i - 1]} start')
    #     tiago_csv_access("cng", car_list[i - 1])
    #
    # time.sleep(4)
    driver.close()

def altroz_imag_csv_access(type,model,i):
    global temp_df

    car=temp_df.loc[(temp_df['Type']==type) & (temp_df['Variant']==model)]
    bookPrice=car['Booking Price'].to_string(index=False)
    showPrice=car['Showroom Price'].to_string(index=False)

    sp_path="/html/body/div[1]/app-root/app-variant-list/div/div[2]/div[3]/div["+str(i)+"]/a/div/div[1]/div[2]"
    cur=driver.find_element(By.XPATH,sp_path)
    price=''.join([i for i in cur.text if i.isdigit()])
    print(price)
    if price!=showPrice: Error_log("altroz",model,type, "none","Showroom Price",price,showPrice,driver.current_url)
    time.sleep(1)
    i=1
    while(True):
       try:
        cur=driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[3]/a[1]")# Book Now
        cur.click()
        time.sleep(4)

        cur=driver.find_element(By.CLASS_NAME,"checkout-btn")
        cur.click()
        time.sleep(3)

        cur=driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-billing-info/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/h3[1]/p") # Checkout Showroom Price
        temp=cur.text
        sp="".join([i for i in temp if i.isdigit()])
        if sp!=showPrice:Error_log("altroz",model,type,"Showroom Price",sp,showPrice,driver.current_url)

        time.sleep(1)
        cur=driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-billing-info/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/ul/li/span") # Checkout Book Price
        temp=cur.text
        bp=''.join([i for i in temp if i.isdigit()])
        if bp!=bookPrice:Error_log("altroz",model,type,"Booking Price",bp,bookPrice,driver.current_url)

        time.sleep(1)
        cur = driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-billing-info/div/div[2]/div/div/div/form/div/div[1]/div/div[1]/div/span") # Checkout Book Price
        temp = cur.text
        bp = ''.join([i for i in temp if i.isdigit()])
        time.sleep(2)
        if bp!=bookPrice:Error_log("altroz",model,type,"Booking Price",bp,bookPrice,driver.current_url)

        print(f'altroz {type} {model} passed')
        driver.back()
        time.sleep(2)

       except:
           break

def altroz_imag_price_check():
    global temp_df

    driver.get(json_data['altroz_imag_url'])
    driver.maximize_window()
    time.sleep(20)

    temp_df=df.loc[df['Car']=='altroz']
    car_list = ["XZ+ Dark", "XZ+ i-TURBO Dark", "XE", "XE+", "XM+", "XT", "XT i-TURBO", "XZ", "XZ i-TURBO", "XZ(O)","XZ+", "XZ+ i-TURBO"]  # Manual list

    for i in range(1,len(car_list)+1):
        temp=i-4
        print(temp)
        while(temp>0):
            cur=driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[2]/a[2]")#Next button
            cur.click()
            temp-=1
        time.sleep(3)
        cur=driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[1]/div[2]/ul/li[2]/a")# Petrol
        cur.click()
        time.sleep(2)
        temp="/html/body/div[1]/app-root/app-variant-list/div/div[2]/div[3]/div["+str(i)+"]/a/div/div[1]/div[1]"
            # "/html/body/div[1]/app-root/app-variant-list/div/div[2]/div[3]/div["+str(i)+"]/a/div/div[1]/div[2]"
            # "/html/body/div[1]/app-root/app-variant-list/div/div[2]/div[3]/div[2]/a/div/div[1]/div[2]"
        cur=driver.find_element(By.XPATH,temp)#Variant
        cur.click()
        temp=cur.text
        sp=''.join([j for j in temp if j.isdigit()])
        time.sleep(2)
        altroz_alt_imag_csv_access("petrol",car_list[i-1],i)

    time.sleep(3)
    for temp in range(0,3):
        cur=driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[2]/a[1]")# Prev Button
        cur.click()
        time.sleep(2)

    car_list = ["XE", "XE+", "XM+", "XT", "XZ", "XZ(O)", "XZ+"]  # Automatic List

    for i in range(1,len(car_list)+1):
        temp=i-4
        print(temp)
        while(temp>0):
            cur=driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[2]/a[2]")#Next button
            cur.click()
            temp-=1
        time.sleep(3)
        cur=driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[1]/div[2]/ul/li[3]/a")# Diesel
        cur.click()
        time.sleep(2)
        temp="/html/body/div[1]/app-root/app-variant-list/div/div[2]/div[3]/div["+str(i)+"]/a/div/div[1]/div[1]"
        cur=driver.find_element(By.XPATH,temp) #Variant
        cur.click()
        time.sleep(2)
        altroz_imag_csv_access("diesel",car_list[i-1])

def altroz_alt_imag_price_check():
    global temp_df,driver

    driver.get(json_data['altroz_imag_url'])
    driver.maximize_window()
    time.sleep(20)

    temp_df = df.loc[df['Car'] == 'altroz']
    car_list = ["XZ+ Dark", "XZ+ i-TURBO Dark", "XE", "XE+", "XM+", "XT", "XT i-TURBO", "XZ", "XZ i-TURBO", "XZ(O)","XZ+", "XZ+ i-TURBO"]  # Manual list
    #
    # for i in range(1,len(car_list)+1):
    #     if i>4:
    #         cur = driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[2]/a[2]")  # Next button
    #         cur.click()
    #     time.sleep(3)
    #     cur = driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[1]/div[2]/ul/li[2]/a")  # Petrol
    #     cur.click()
    #     time.sleep(2)
    #     temp = "/html/body/div[1]/app-root/app-variant-list/div/div[2]/div[3]/div[" + str(i) + "]/a/div/div[1]/div[1]"
    #     cur=driver.find_element(By.XPATH,temp)
    #     cur.click()
    #     time.sleep(2)
    #     altroz_alt_imag_csv_access("petrol",car_list[i-1],i)
    #
    # time.sleep(3)
    # for temp in range(0, 3):
    #     cur = driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[2]/a[1]")  # Prev Button
    #     cur.click()
    #     time.sleep(2)

    car_list = ["XE", "XE+", "XM+", "XT", "XZ", "XZ(O)", "XZ+"]  # Automatic List

    for i in range(1, len(car_list) + 1):
        if i>4:
            cur = driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[2]/a[2]")  # Next button
            cur.click()
        time.sleep(3)
        cur = driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[1]/div[2]/ul/li[3]/a")  # Diesel
        cur.click()
        time.sleep(2)
        temp = "/html/body/div[1]/app-root/app-variant-list/div/div[2]/div[3]/div[" + str(i) + "]/a/div/div[1]/div[1]"
        cur = driver.find_element(By.XPATH, temp)  # Variant
        cur.click()
        time.sleep(2)
        altroz_alt_imag_csv_access("diesel", car_list[i - 1],i)

def altroz_alt_imag_csv_access(type, model, i):
    global temp_df,driver
    car = temp_df.loc[(temp_df['Type'] == type) & (temp_df['Variant'] == model)]
    bookPrice = car['Booking Price'].to_string(index=False)
    showPrice = car['Showroom Price'].to_string(index=False)

    sp_path = "/html/body/div[1]/app-root/app-variant-list/div/div[2]/div[3]/div[" + str(i) + "]/a/div/div[1]/div[2]"
    cur = driver.find_element(By.XPATH, sp_path)
    price = ''.join([i for i in cur.text if i.isdigit()])
    print(price)
    if price != showPrice: Error_log("altroz", model, type, "none", "Showroom Price", price, showPrice,driver.current_url)
    time.sleep(1)
    i = 1
    cur = driver.find_element(By.XPATH, "/html/body/div[1]/app-root/app-variant-list/div/div[3]/a[1]")  # Book Now
    cur.click()
    time.sleep(4)
    while (True):
        try:
            xpath="/html/body/div[1]/app-root/app-variant-list/div/div[3]/div/div/div/div[3]/ul/li["+str(i)+"]"
            cur=driver.find_element(By.XPATH,xpath)
            cur.click()
            time.sleep(2)
            i+=1

        except:
            break

    cur=driver.find_element(By.XPATH,"/html/body/div[1]/app-root/app-variant-list/div/div[3]/div/div/div/div[1]")
    cur.click()
    time.sleep(2)

def tr():
    global json_data
    f = open('D:/EE/PriceCheck/Tata/TataSettings.json')
    json_data = json.load(f)
    #for i in json_data.keys():
     #   print(i, ":", json_data[i])
    f.close()

json_data=dict()
tr()
cols=["Car","Type","Variant","Booking Price","Showroom Price","Acc"]
df=pd.read_csv(json_data["prices_csv_path"],usecols=cols)
temp_df=pd.DataFrame()
s=Service(json_data["service_path"])
chrome_options = webdriver.ChromeOptions().add_argument('--proxy-server=%s' % json_data["proxy"])
driver=webdriver.Chrome(service=s,chrome_options=chrome_options)
def initialise():
    global s,driver,chrome_options
    driver=webdriver.Chrome(service=s,chrome_options=chrome_options)

try:
    # if json_data['tiago_check']=='Y':
    #     tiago_price_check()
    # if json_data['tigor_check']=='Y':
    #     tigor_price_check()
    # if json_data['safari_check']=='Y':
    #     safari_price_check()
    # if json_data['punch_check']=='Y':
    #     punch_price_check()
    # if json_data['altroz_check']=='Y':
    #     altroz_alt_imag_price_check()
    # if json_data['harrier_check']=='Y':
    #     harrier_price_check()
    # if json_data['tigor_ev_check']=='Y':
    #     tigor_ev_price_check()
    # if json_data['altroz_imag_check']=='Y':
    #     altroz_alt_imag_price_check()
    safari_imag_price_check()
finally:
    driver.quit()