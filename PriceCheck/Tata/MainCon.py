import json
from PriceCheck.Tata.tiago import tiago_start
from PriceCheck.Tata.punch import punch_start
from PriceCheck.Tata.altroz import altroz_start
from PriceCheck.Tata.safari import safari_start
from PriceCheck.Tata.harrier import harrier_start
from PriceCheck.Tata.tigor import tigor_start
from PriceCheck.Tata.tigor_ev import tigor_ev_start
from PriceCheck.Tata.nexon_imag import nexon_imag_start
from PriceCheck.Tata.altroz_imag import altroz_imag_start

def start():
    f = open('TataSettings.json')
    json_data = json.load(f)
    f.close()
    try:
        if json_data['tiago_check'] == 'Y': tiago_start()
    except Exception as err: print('Issue with tiago\n',err)

    try:
        if json_data['tigor_check'] == 'Y':tigor_start()
    except Exception as err:print('Issue with tiago\n',err)
    try:
        if json_data['safari_check'] == 'Y':safari_start()
    except Exception as err:print("Issue with Safari\n",err)

    try:
        if json_data['punch_check'] == 'Y': punch_start()
    except Exception as err: print('Issue with punch\n',err)

    try:
        if json_data['altroz_check'] == 'Y': altroz_start()
    except Exception as err:print('Issue with altroz\n',err)

    try:
        if json_data['harrier_check'] == 'Y':harrier_start()
    except Exception as err:print("Issue with harrier\n",err)
    try:
        if json_data['tigor_ev_check'] == 'Y':tigor_ev_start()
    except Exception as err:print('Issue with tigor ev\n',err)

    # try:
    #     if json_data['nexon_imag_check']=='Y':nexon_imag_start()
    # except Exception as err:print('Issue with nexon imag\n',err)

    # try:
    #     if json_data['altroz_imag_check']=='Y': altroz_imag_start()
    # except Exception as err:print('Issues with altroz imag\n',err)

start()