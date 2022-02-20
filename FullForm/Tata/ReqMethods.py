import csv

def Error_log(car_name,model_name,type,colour,price_type,listed_price,actual_price,url,error_path):
    print(car_name,model_name,type,colour,price_type,listed_price,actual_price,url,"FAIL")
    with open(error_path,'a') as f:
        w=csv.writer(f)
        w.writerow([car_name,model_name,type,colour,price_type,listed_price,actual_price,url])
        print("Write done")