import json
from FullForm.Tata.tiago import tiago_start
from FullForm.Tata.tigor import tigor_start
from FullForm.Tata.harrier import harrier_start
from FullForm.Tata.TigorEV import tigor_ev_start
from FullForm.Tata.altroz import altroz_start
from FullForm.Tata.punch import punch_start
from FullForm.Tata.safari import safari_start

def run_checks():
    json_data = dict()
    #print("in")
    f = open('TataSettings.json')
    json_data = json.load(f)
    f.close()
    if json_data['tiago_check']=='Y':
        tiago_start()
    if json_data['tigor_check']=='Y':
        tigor_start()
    if json_data['harrier_check']=='Y':
        harrier_start()
    if json_data['altroz_check']=='Y':
        altroz_start()
    if json_data['safari_check']=='Y':
        safari_start()
    if json_data['punch_check']=='Y':
        punch_start()
    if json_data['tigor_ev_check']=='Y':
        tigor_ev_start()

run_checks()