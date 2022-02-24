import os,sys
try:sys.path.append(os.path.dirname(os.getcwd()))
except:print('Issue with assigning path')

import json
from Tata.TataDealerChecks import tata_dealer_checks_start
from Tata.EVDealerCheck import ev_dealer_check_start

def start():
    car_list = ["safari_imag", "punch", "nexon_imag", "altroz", "safari", "altroz_imag","harrier", "tigor", "tiago"]
    f = open('TataSettings.json')
    json_data = json.load(f)
    f.close()

    for i in car_list:
        if json_data[i+'_check']=='Y': tata_dealer_checks_start(i)

    car_list = ["nexon_ev", "tigor_ev"]
    for i in car_list:
        if json_data[i+'_check']=='Y': ev_dealer_check_start(i)

start()
sys.path.remove(os.getcwd())
